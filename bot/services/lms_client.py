"""LMS API client for fetching backend data.

Uses Bearer token authentication. Handles errors gracefully.
"""

import httpx
from typing import Optional, Any


class LMSClient:
    """Client for the LMS backend API."""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._client: Optional[httpx.Client] = None

    def _get_client(self) -> httpx.Client:
        """Get or create HTTP client with auth headers."""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10.0,
            )
        return self._client

    def health_check(self) -> dict[str, Any]:
        """Check backend health by fetching items count.
        
        Returns:
            dict with 'healthy' bool and 'message' str
        """
        try:
            client = self._get_client()
            response = client.get("/items/")
            response.raise_for_status()
            items = response.json()
            return {
                "healthy": True,
                "message": f"Backend is healthy. {len(items)} items available.",
            }
        except httpx.ConnectError as e:
            return {
                "healthy": False,
                "message": f"Backend error: connection refused. Check that services are running.",
            }
        except httpx.HTTPStatusError as e:
            return {
                "healthy": False,
                "message": f"Backend error: HTTP {e.response.status_code}. The backend service may be down.",
            }
        except Exception as e:
            return {
                "healthy": False,
                "message": f"Backend error: {str(e)}",
            }

    def get_labs(self) -> list[dict[str, Any]]:
        """Get all labs from the backend.
        
        Returns:
            List of lab objects with id, title, type
        """
        try:
            client = self._get_client()
            response = client.get("/items/")
            response.raise_for_status()
            items = response.json()
            # Filter only labs
            return [item for item in items if item.get("type") == "lab"]
        except Exception:
            return []

    def get_pass_rates(self, lab_id: str) -> dict[str, Any]:
        """Get pass rates for a specific lab.
        
        Args:
            lab_id: Lab identifier (e.g., "lab-04")
            
        Returns:
            dict with 'success' bool, 'data' list, 'error' str
        """
        try:
            client = self._get_client()
            # First, find the lab by title/ID
            labs = self.get_labs()
            lab = None
            for l in labs:
                # Match by ID pattern or title
                if f"lab-{lab_id.replace('lab-', '')}" in l.get("title", "").lower() or \
                   l.get("id") == int(lab_id.replace("lab-", "")) if lab_id.replace("lab-", "").isdigit() else False:
                    lab = l
                    break
            
            if not lab:
                # Try direct lookup by assuming lab-XX maps to id XX
                try:
                    lab_num = int(lab_id.replace("lab-", ""))
                    for l in labs:
                        if l.get("id") == lab_num:
                            lab = l
                            break
                except (ValueError, AttributeError):
                    pass
            
            if not lab:
                return {
                    "success": False,
                    "error": f"Lab '{lab_id}' not found.",
                    "data": [],
                }
            
            # Get analytics for this lab
            lab_title = lab.get("title", "")
            response = client.get("/analytics/pass-rates", params={"lab": lab_title})
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "data": data,
                "error": None,
            }
        except httpx.ConnectError:
            return {
                "success": False,
                "error": "Backend connection refused.",
                "data": [],
            }
        except httpx.HTTPStatusError as e:
            return {
                "success": False,
                "error": f"HTTP {e.response.status_code}: {e.response.text}",
                "data": [],
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": [],
            }

    def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            self._client.close()
            self._client = None

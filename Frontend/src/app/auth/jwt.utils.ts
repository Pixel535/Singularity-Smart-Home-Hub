export function isTokenExpired(token: string): boolean {
    if (!token) return true;
  
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const expiry = payload.exp;
      const now = Math.floor(Date.now() / 1000);
      return now >= expiry;
    } catch (e) {
      return true;
    }
  }
  
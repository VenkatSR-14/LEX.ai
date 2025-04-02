// Token utility to check expiry
export const isTokenExpired = (token: string | null): boolean => {
    if (!token) return true;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      console.log('Decoded Token Payload:', payload);
      return Date.now() >= payload.exp * 1000;
    } catch {
      return true;
    }
  };
  
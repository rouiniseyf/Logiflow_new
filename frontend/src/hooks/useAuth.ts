import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

interface AuthTokens {
  refresh: string;
  access: string;
}

const useAuth = (): any => {
  const [isAuthenticated, setIsAuthenticated] = useState(true);
  const [user, setUser] = useState(null)
  const navigate = useNavigate()
  useEffect(() => {
    const checkAuth = () => {
      
      // Check if auth tokens are present in local storage
      const authTokensJSON = localStorage.getItem('authTokens');

      if (authTokensJSON) {
        try {
          // Parse the JSON containing both access and refresh tokens
          const tokens: AuthTokens = JSON.parse(authTokensJSON);

          // Decode the access token
          const decodedAccessToken: any = JSON.parse(atob(tokens.access.split('.')[1]));

          // Check if the access token is expired
          const isAccessTokenExpired: boolean = decodedAccessToken.exp * 1000 < Date.now();
          if(isAccessTokenExpired) navigate("/login")

          setUser(decodedAccessToken.user);

          // Update the connected state based on the access token expiration
          setIsAuthenticated(!isAccessTokenExpired);
        } catch (error) {
          console.error('Error decoding or checking access token:', error);
          setIsAuthenticated(false);
        }
      } else {
        // No auth tokens found in local storage
        navigate("/login")
        setIsAuthenticated(false);
      }
    };

    // Call the checkAuth function when the component mounts
    checkAuth();

    // You can also set up interval to periodically check the token if needed
    const intervalId = setInterval(checkAuth, 10000); // Check every minute

    // Cleanup function to clear the interval if the component unmounts
    return () => clearInterval(intervalId);

  }, []); // Empty dependency array ensures the effect runs only once on mount

  return {isAuthenticated,user};
};

export default useAuth;

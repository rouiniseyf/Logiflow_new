import axios from "axios";

type useAxiosProps = {
  includeToken? :boolean 
}
const useAxios = ({includeToken}:useAxiosProps ={}) => {

  const baseURL = `http://localhost:8000`

  let authTokens:any = localStorage.getItem('authTokens')
  authTokens = JSON.parse(authTokens)
  const axiosInstance = axios.create({
      baseURL,
  });

  if (includeToken) {
    axiosInstance.defaults.headers.common['Authorization'] = `JWT ${authTokens?.access}`;
  }

  return axiosInstance
}

export default useAxios;
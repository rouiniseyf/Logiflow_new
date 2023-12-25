import React, {useState} from "react";
import logo from "../assets/logo.svg";
import white_logo from "../assets/logo_white.svg";
import {useNavigate } from "react-router-dom"
import useAxios from "../hooks/useAxios";



type FormData = {
  username: string, 
  password: string
}
type FormProps = {
  onFormSubmit: (data:FormData) => void;
}

const Login = () => {
  const api = useAxios()

  const navigate = useNavigate();

  const [passwordDispaly, setPasswordDisplay] = useState<Boolean>(false)
  const taggolPasswordDispaly = () => {
    setPasswordDisplay(!passwordDispaly)
  }

  const handleLogin = (formData:FormData) =>{

    api.post("/api/auth/token/", formData).then(data => {
        console.log(data)
        // Assuming the auth token is present in the response as 'token'
       
        // Save the auth token to localStorage
        localStorage.setItem('authTokens',  JSON.stringify(data))
    
        navigate("/");
        console.log('Authentication successful! Auth token saved to localStorage.');
      })
      .catch(error => {
        console.error('Authentication error:', error.message);
      });

  }



  const hadnleSumit = (e:React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const username = (document.getElementById('username') as HTMLInputElement).value;
    const password = (document.getElementById('password') as HTMLInputElement).value;

    const formData: FormData = { username, password };

    handleLogin(formData)
  }

  return (
    <div className="h-[100vh] w-full flex justify-center items-center">
      <div className="h-[400px] w-[400px]  rounded-3xl  flex flex-col justify-center items-center p-5 ga">
        <div className="h-[15vh] flex justify-center items-center dark:hidden mb-6">
          <img src={logo} width={120} height={120}></img>
        </div>
        <div className="h-[15vh] flex-col justify-center items-center hidden dark:flex mb-6">
          <img src={white_logo} width={120} height={120}></img>
        </div>
        <div className="divider">Connexion</div>

        <div>
        <form onSubmit={hadnleSumit}>
          <input
            type="text"
            id="username"
            placeholder="Nom d'utilisateur"
            className="input input-md  input-bordered w-full rounded-2xl"
          />
          <input
            id="password"
            type={passwordDispaly?"text":"password"}
            placeholder="Mot de pass"
            className="input input-md input-bordered w-full mt-3 rounded-2xl"
          />
          <div className="flex justify-end m-2 "><button className="btn btn-xs" onTouchStart={taggolPasswordDispaly} onTouchEnd={taggolPasswordDispaly} onMouseDown={taggolPasswordDispaly} onMouseUp={taggolPasswordDispaly}>Afficher le mot de passe</button></div>
          <button type="submit" className="btn w-full mt-3 rounded-2xl">Se connecter </button>
          </form>
        </div>
       
      </div>
    </div>
  );
};

export default Login;

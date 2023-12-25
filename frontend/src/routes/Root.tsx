import React, { useEffect, useState } from "react";
import SideBar from "../sidebar/SideBar";
import { Outlet, useNavigate } from "react-router-dom";
import ThemeSwitch from "../components/ThemeSwitch";
import { ConfigProvider, theme, Button, Card } from "antd";
import useAuth from "../hooks/useAuth";
import MobileSideBar from "../sidebar/components/MobileSideBar";

const Root = () => {
  const {isAutenticated} = useAuth()

  const { defaultAlgorithm, darkAlgorithm } = theme;
  const [localTheme, setLocalTheme] = useState("dark");


  return (
    <ConfigProvider
    theme={{
      algorithm: localTheme==="dark" ? darkAlgorithm : defaultAlgorithm,
      token:{borderRadius: 10},
      components:{
        Button:{
          primaryShadow: "none", 
          boxShadow:"none", 
          controlOutline:"none", 
        }
      }
    }} 
    >
    <div className="flex w-full h-[100vh]" data-theme={localTheme}>
      <div className="flex-None w-[260px] h-full bg-gray-100 dark:bg-base-200 lg:block hidden">
        <SideBar />
      </div>

      <div className="dark:bg-base-100 bg-white grow h-full">
        <MobileSideBar />
        <ThemeSwitch localTheme={localTheme} setLocalTheme={setLocalTheme}/>
        <Outlet />
      </div>
    </div>
    </ConfigProvider>
  );
};

export default Root;

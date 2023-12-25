import SideBar from "../SideBar";
import logo from "../../assets/logo_collapsed.svg";

const MobileSideBar = () => {
  return (
    <div className="drawer z-10">
      <input id="my-drawer" type="checkbox" className="drawer-toggle" />
      <div className="drawer-content flex flex-row  absolute left-4 top-4  lg:hidden items-center">
        <div className="w-[40px] h-[40px]">
          <label
            htmlFor="my-drawer"
            className="btn btn-xs rounded-[10px] drawer-button w-[40px] h-[40px]"
          >
            
            <img src={logo} width={20} height={20}></img>
          </label>
        
        </div>
       <span className="ml-2 font-semibold text-primary dark:text-gray-400">LOGIFLOW</span>
      </div>
      <div className="drawer-side">
        <label
          htmlFor="my-drawer"
          aria-label="close sidebar"
          className="drawer-overlay text-white"
        ></label>
        <div className="w-[250px] bg-base-200">
          <SideBar />
        </div>
      </div>
    </div>
  );
};

export default MobileSideBar;

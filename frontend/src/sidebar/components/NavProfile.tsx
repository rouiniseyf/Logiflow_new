import useAuth from "../../hooks/useAuth";
import { Popconfirm } from "antd";
import { useNavigate } from "react-router-dom";

const NavProfile = () => {

    const { user } = useAuth();

    const User = () => {
        return (
          <>
            <span className="mb-2 text-[8pt]">
              {user?.first_name} {user?.last_name}
            </span>
          </>
        );
      };

      const navigate = useNavigate();

      const handleLogout = () => {
        localStorage.removeItem("authTokens");
        navigate("/login");
      };

  return (
    <>
    <div>
          <div className="avatar flex justify-center items-center mt-6 mb-4 ">
            <div className="w-16 mask mask-hexagon">
              <img src="https://daisyui.com/images/stock/photo-1534528741775-53994a69daeb.jpg" />
            </div>
          </div>
        </div>
        <div className="flex justify-center ">{user ? <User /> : <></>}</div>
        <Popconfirm
          placement="topLeft"
          title="Déconnexion"
          description="Do you really want to deconnect"
          okText="Yes"
          cancelText="No"
          onConfirm={handleLogout}
          okButtonProps={{
            className:
              "bg-primary hover:bg-green-800 text-white dark:bg-base-200 dark:hover:bg-gray-800",
          }}
        >
          <button className="btn btn-sm w-fit text-[9pt] border-1 dark:border-neutral-700 border-neutral-400 font-normal rounded-full px-4 mb-4">
            déconnecter
          </button>
        </Popconfirm>
    </>
  )
}

export default NavProfile
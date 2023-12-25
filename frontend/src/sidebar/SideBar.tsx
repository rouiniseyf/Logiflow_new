import logo from "../assets/logo.svg";
import white_logo from "../assets/logo_white.svg";
import NavItem from "../sidebar/components/NavItem";
import NavProfile from "./components/NavProfile";

const SideBar = () => {


  return (
    <div>
      <div className="h-[15vh] flex justify-center items-center dark:hidden">
        <img src={logo} width={80} height={80}></img>
      </div>
      <div className="h-[15vh] justify-center items-center hidden dark:flex">
        <img src={white_logo} width={80} height={80}></img>
      </div>
      <div className="h-[60vh] overflow-y-auto overflow-x-hidden scrollbar scrollbar-thumb-green-700  dark:scrollbar-thumb-gray-600 scrollbar-thumb-opacity-[20%] scrollbar-thumb-rounded-[50px] scrollbar-w-[8px]">
        <ul className="menu  w-56 scrollbar-thumb-green-600">
          <NavItem type="simple" to="/" text="Tableau de bord" />
          <NavItem
            type="nested"
            to=""
            text="Prestations"
            children={[
              { text: "Groupage", to: "/prestations/groupage" },
              { text: "Cotneneur", to: "/prestations/conteneur" },
            ]}
          />
          <NavItem type="simple" to="/gros" text="Gros" />
          <NavItem
            type="nested"
            to=""
            text="References"
            children={[
              { text: "Client", to: "1" },
              { text: "Direction", to: "2" },
              { text: "Transitaire", to: "3" },
              { text: "Consignataire", to: "4" },
              { text: "Armateur", to: "5" },
              { text: "Banque", to: "6" },
              { text: "Zone", to: "7" },
              { text: "Box", to: "8" },
            ]}
          />

        </ul>
      </div>
      <div className="h-[25vh] flex flex-col justify-end items-center mb-4 select-none">
        <NavProfile />
      </div>
    </div>
  );
};

export default SideBar;

import { NavLink } from "react-router-dom";

type NavItemType = {
  to: string;
  text: string;
};

type NavItemPropsType = {
  type: "simple" | "nested";
  text: string;
  to: string;
  children?: NavItemType[];
};

const NavItem = (props: NavItemPropsType) => {
  const { type, text, to, children } = props;
  return (
    <>
      {type === "simple" ? (
        <li>
          <NavLink to={to}>{text}</NavLink>
        </li>
      ) : (
        <li>
          <a>{text}</a>
          <ul>
            {children?.map((child) => (
              <li>
                <NavLink to={child.to}>{child.text}</NavLink>
              </li>
            ))}
          </ul>
        </li>
      )}
    </>
  );
};

export default NavItem;

import Item from "antd/es/list/Item";
import React from "react";
import { NavLink } from "react-router-dom";

type NavLinkType = {
  text: string;
  to : "/" | string;
  link: boolean;
};

type NavItemProps = {
  data: NavLinkType;
};

type BreadcrumbsProps = {
    data: NavLinkType[];
  };
  
const Breadcrumbs = ({data}: BreadcrumbsProps) => {
  const NavItem = ({ data }: NavItemProps) => {
    if (data.link) {
    return <li>
        <NavLink key={data.text} to={data.to}>{data.text}</NavLink>
      </li>;
    }
    return <li key={data.text}>{data.text}</li>;
  };
  return (
    <div className="text-sm breadcrumbs absolute top-4 hidden lg:block">
      <ul>
        {data.map((item, index) => {return <NavItem key={index} data={item}></NavItem>})}
      </ul>
    </div>
  );
};

export default Breadcrumbs;

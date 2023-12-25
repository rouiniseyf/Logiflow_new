import { useEffect,memo  } from "react";
import { BiMoon, BiSun } from "react-icons/bi";

function ThemeSwitch({localTheme,setLocalTheme}) {


  const setTheme = (value: string) => {
    setLocalTheme(value);
    localStorage.setItem("theme", value);
  };

  const taggoleTheme = () => {
    setTheme(localStorage.getItem("theme") === "dark" ? "light" : "dark");
  };

  useEffect(() => {
    const theme = localStorage.getItem("theme");
    if (!theme) {
      if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
        setTheme("dark");
        document.documentElement.classList.remove("dark", "light");
        document.documentElement.classList.add("dark");
      }
      if (window.matchMedia("(prefers-color-scheme: light)").matches) {
        setTheme("light");
        document.documentElement.classList.remove("dark", "light");
        document.documentElement.classList.add("light");
      }
    } else {
      if (theme === "light") {
        setTheme("light");
        document.documentElement.classList.remove("dark", "light");
        document.documentElement.classList.add("light");
      } else {
        setTheme("dark");
        document.documentElement.classList.remove("dark", "light");
        document.documentElement.classList.add("dark");
      }
    }
  }, [localTheme]);

  return (
    <div className="absolute top-4 right-4 z-20">
      <button
        className="btn btn-xs rounded-[10px]"
        style={{width:"40px", height:"40px"}}
        onClick={taggoleTheme}
      >
        {localTheme === "dark" ? <BiMoon className="w-[20px] h-[20px]" /> : <BiSun className="w-[20px] h-[20px]"/>}
      </button>
    </div>
  );
}

export default memo(ThemeSwitch);

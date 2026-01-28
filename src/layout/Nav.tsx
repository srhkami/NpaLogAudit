import BtnThemeToggle from "./BtnThemeToggle.tsx";
import ModalChangelog from "@/features/About/ModalChangelog.tsx";
import {Dropdown, DropdownToggle, DropdownContent} from "@/component";
import {HiMenuAlt2} from "react-icons/hi";
import ModalReadme from "@/features/About/ModalReadme.tsx";

export default function Nav() {

  return (
    <div className="navbar bg-base-100 shadow-sm sticky top-0 z-20">
      <div className="navbar-start">
        <Dropdown>
          <DropdownToggle style='ghost' shape='circle' dropdownIcon={false}>
            <HiMenuAlt2 className="h-5 w-5"/>
          </DropdownToggle>
          <DropdownContent>
            <ul className="menu">
              <li>
                <ModalReadme/>
              </li>
              <li>
                <ModalChangelog/>
              </li>
            </ul>
          </DropdownContent>
        </Dropdown>
      </div>
      <div className="navbar-center">
        <a className="btn btn-ghost text-xl">日誌稽核小鴿手</a>
      </div>
      <div className="navbar-end">
        <BtnThemeToggle/>
      </div>
    </div>
  )
}
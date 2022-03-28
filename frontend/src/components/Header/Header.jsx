import React from 'react';
import {Link, useResolvedPath, useMatch} from "react-router-dom";

import {URL_HOME, URL_LOGIN, URL_ABOUT} from "../../app/const";

import styles from './styles.module.scss';

function CustomLink({children, to, ...props}) {
    let resolved = useResolvedPath(to);
    let match = useMatch({ path: resolved.pathname, end: true });

    return (
        <Link className={match ? `${styles['link']} ${styles.active}` : styles['link']} to={to} {...props} >
            {children}
        </Link>
    )
}

function Header(props) {

    return (
        <header className={styles['app-header']}>
            <h1 className={styles['header-logo']}> Team Strays in Tokyo </h1>
            <nav className={styles['header-nav']}>
                <ul className={styles['header-ul']}>
                    <li className={styles['header-li']}><CustomLink to={URL_HOME}>HOME</CustomLink></li>
                    <li className={styles['header-li']}><CustomLink to={URL_LOGIN}>LOGIN</CustomLink></li>
                    <li className={styles['header-li']}><CustomLink to={URL_ABOUT}>ABOUT</CustomLink></li>
                </ul>
            </nav>

        </header>
    )
}

export default Header;

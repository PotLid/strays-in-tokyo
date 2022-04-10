import React from 'react';

import styles from './styles.module.scss';

import stars from '../../imgs/stars.svg';
import moon from '../../imgs/moon.svg';
import mt_behind from '../../imgs/mountains_behind.svg';
import mt_front from '../../imgs/mountains_front.svg';

function Background(props) {

    return (
        <div className={`${styles['app-background']}`}>
            <img src={stars} alt={'bg-stars'} />
            <img className={styles.blend} src={moon} alt={'bg-moon'} />
            <img src={mt_behind} alt={'bg-mountain-behind'} />
            <img src={mt_front} alt={'bg-mountain-front'} />
        </div>
    )
}

export default Background;

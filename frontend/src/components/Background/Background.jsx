import React from 'react';

import styles from './styles.module.scss';

import stars from '../../imgs/stars.png';
import moon from '../../imgs/moon.png';
import mt_behind from '../../imgs/mountains_behind.png';
import mt_front from '../../imgs/mountains_front.png';

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

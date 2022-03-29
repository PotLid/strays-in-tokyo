import React from 'react';

import styles from './styles.module.scss';

import bird from '../../imgs/rage_bird.gif';

function NotFound(props) {

    return (
        <section className={styles['view-not-found']}>
            <div className={styles['message-wrap']}>
                <div className={styles['contents']}>
                    <img src={bird} alt={'rage bird'}/>
                    <h2>Page Not Found</h2>
                </div>
            </div>
        </section>
    )
}

export default NotFound;

import React, {useState} from 'react';

import styles from './styles.module.scss';

function Chat() {

    return (
        <section className={styles['view-chat']}>
            <div className={styles['container']}>

                <div className={styles['users']}>
                    <div className={styles['header']}>
                        <h2>Online users</h2>
                    </div>

                    <div className={styles['online_users']}>
                        <ul className={styles['list_users']}>
                            <li>Squeaks</li>
                            <li>Duck</li>
                        </ul>
                    </div>
                </div>


                <div className={styles['container2']}>

                    <div className={styles['chat_box']}>
                        <p className={styles['message']}> Hello </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                        <p className={styles['user_message']}> What's up? </p>
                    </div>

                    <div className={styles['footer']}>
                        <form className={styles['form_chat']}>
                            <input type="text" name=""/>
                                <button onClick={e => e.preventDefault()}> SEND ➤</button>
                        </form>
                    </div>

                </div>
            </div>
        </section>
    )
}

export default Chat;

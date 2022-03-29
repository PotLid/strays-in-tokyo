import React, {useState} from 'react';

import styles from './styles.module.scss';

function LoginForm({setSignUp}) {

    const custom_clk = (e) => {
        e.preventDefault();
        setSignUp();
    }

    return (
        <form className={styles['form-login']}>
            <h1 className={styles['form-title']}>Ready to Log in?</h1>
            <p className={styles['form-desc']}>You're almost there!</p><br/><br/>

            <div className={styles['form-group']}>
                <label className={styles['form-label']} htmlFor={'form-email'}>Email</label>
                <input className={styles['form-input']} type={'text'} name={'form-email'} placeholder={''}/>
            </div>

            <div className={styles['form-group']}>
                <label className={styles['form-label']} htmlFor={'form-pw'}>Password</label>
                <input className={styles['form-input']} type={'password'} name={'form-pw'} placeholder={''}/>
            </div>

            <input className={styles['form-btn']} type={'submit'} value={'Sign in'} /><br/>
            <button onClick={custom_clk}>Do you need to sign up for the account?</button>
        </form>
    )
}

const SignUpForm = ({setLogin}) => {

    const custom_clk = (e) => {
        e.preventDefault();
        setLogin();
    }

    return (
        <form className={styles['form-signup']}>
            <h1 className={styles['form-title']}>Ready to Sign up?</h1>
            <p className={styles['form-desc']}>Create an account below!</p><br/><br/>

            <div className={styles['form-group']}>
                <label className={styles['form-label']} htmlFor={'form-email'}>Email</label>
                <input className={styles['form-input']} type={'text'} name={'form-email'} placeholder={''} autoComplete={'off'}/>
            </div>

            <div className={styles['form-group']}>
                <label className={styles['form-label']} htmlFor={'form-pw'}>Password</label>
                <input className={styles['form-input']} type={'password'} name={'form-pw'} placeholder={''} autoComplete={'off'}/>
            </div>

            <div className={styles['form-group']}>
                <label className={styles['form-label']} htmlFor={'form-confirm-pw'}>Confirm Password</label>
                <input className={styles['form-input']} type={'password'} name={'form-confirm-pw'} placeholder={''} autoComplete={'off'}/>
            </div>

            <input className={styles['form-btn']} type={'submit'} value={'Sign up'} /><br/>
            <button onClick={custom_clk}>Go back to the login.</button>
        </form>
    )
}

function Login(props) {
    const [isSignUp, setSignUp] = useState(false);

    const getLogin = () => {setSignUp(false)}
    const getSignUp = () => {setSignUp(true)}

    return (
        <section className={styles['view-login']}>
            <div className={styles['form-wrap']}>
                {!isSignUp ? <LoginForm setSignUp={getSignUp} /> : <SignUpForm setLogin={getLogin} />}
            </div>
        </section>
    )
}

export default Login;

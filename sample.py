import streamlit as st
import math

st.title("Welcome to CPF Retirement Calculator for the Not So Old! :full_moon_with_face:")
st.caption("Please note that this is a simplified calculator where we assume no salary increment and no interest changes. This is not an official calculator by CPFB")
st.caption("To view your results, please fill in all relevant details")

def cpf_retirement_calculator(age, income, oa_balance, sa_balance, ma_balance, flat_value,percent_of_OA,flat_age):
    frs=False
    retirement_age = 65
    ra_balance = 0
    annual_contribution = income * 12 * 0.37
    for current_age in range(age, retirement_age):
        if current_age == flat_age:
            oa_balance = oa_balance - flat_value * percent_of_OA
        if current_age<=35:
            oa_balance += annual_contribution * 0.6217
            sa_balance += annual_contribution * 0.1621
            ma_balance += annual_contribution * 0.2162
            oa_balance = oa_balance * (1+2.5/100)
            sa_balance = sa_balance * (1+4/100)
            ma_balance = ma_balance * (1+4/100)
        elif current_age<=44:
            oa_balance += annual_contribution * 0.5677
            sa_balance += annual_contribution * 0.1891
            ma_balance += annual_contribution * 0.2432
            oa_balance = oa_balance * (1+2.5/100)
            sa_balance = sa_balance * (1+4/100)
            ma_balance = ma_balance * (1+4/100)
        elif current_age<=49:
            oa_balance += annual_contribution * 0.5136
            sa_balance += annual_contribution * 0.2162
            ma_balance += annual_contribution * 0.2702
            oa_balance = oa_balance * (1+2.5/100)
            sa_balance = sa_balance * (1+4/100)
            ma_balance = ma_balance * (1+4/100)
        elif current_age<=54:
            oa_balance += annual_contribution * 0.4055
            sa_balance += annual_contribution * 0.3108
            ma_balance += annual_contribution * 0.2837
            oa_balance = oa_balance * (1+2.5/100)
            sa_balance = sa_balance * (1+4/100)
            ma_balance = ma_balance * (1+4/100)
        elif current_age<=59:
            if current_age==55:
                if sa_balance>=198800:
                    ra_balance+=198800
                    sa_balance-=198800
                else:
                    ra_balance=sa_balance
                    sa_balance=0
                    remaining = 198800-ra_balance
                    if oa_balance>=remaining:
                        ra_balance+=remaining
                        oa_balance-=remaining
                    elif oa_balance>=0:
                        ra_balance+=oa_balance
                        oa_balance=0
                if ra_balance==198800:
                    frs=True
            oa_balance += annual_contribution * 0.4069
            sa_balance += annual_contribution * 0.2372
            ma_balance += annual_contribution * 0.3559
            oa_balance = oa_balance * (1+2.5/100)
            sa_balance = sa_balance * (1+4/100)
            ma_balance = ma_balance * (1+4/100)
            ra_balance= ra_balance * (1+4/100)
        else:
            oa_balance += annual_contribution * 0.1709
            sa_balance += annual_contribution * 0.317
            ma_balance += annual_contribution * 0.5121
            oa_balance = oa_balance * (1+2.5/100)
            sa_balance = sa_balance * (1+4/100)
            ma_balance = ma_balance * (1+4/100)
            ra_balance= ra_balance * (1+4/100)
    return [ra_balance,frs]

def cpf_topup(age, income):
    a = 1.04*(1-1.04**(55-age))/(1-1.04)
    b = 198800/a
    c = b - income * 12 * 0.37 * 0.2
    return c/(30*12)
age_1,age_2=st.columns(2)

with age_1:
    age = st.text_input("Age")
with age_2:
    st.success("It is never too early to start planning for your retirement! :100:")

st.write("")
st.write("")
st.write("What is your current CPF balance?")
st.caption("You may check your balance on the CPF website or application")
oa,sa,ma = st.columns(3)
with oa:
    oa_balance = st.text_input("Ordinary Account")
with sa:
    sa_balance = st.text_input("Special Account")
with ma:
    ma_balance = st.text_input("Medisave Account")
    
st.write("")
st.write("") 
work = st.radio("Are you currently contributing to CPF?",("Yes","No"))

if work=="Yes":
    col1,col2 = st.columns(2)
    salary = col1.text_input("How much do you earn per month?")
    col2.info("Eh u know ornot? :thinking_face:")
    col2.warning("You contribute 20% of your base salary to your CPF while your boss contribute 17% of your base salary to your CPF")
else:
    col3,col4 = st.columns(2)
    avg_wage=col3.radio("Do you wish to continue using the average wage earned in Singapore",("Yes","No"))
    if avg_wage=="Yes":
        salary=4000
        col4.info("Eh u know ornot? :thinking_face:")
        col4.warning("In 2023, the average wage earned per month is $4000")
    else:
        st.info("Aww we are sad to see you go :cry: But it's ok if you are still uncertain about retirement! You are not alone :handshake: We have compiled some fun facts about CPF and Retirement under this section. For more, feel free to vist our website or contact us!")
        with st.expander("Click to view some fun facts of CPF!"):
            st.warning("When you turn 55, you can withdraw $5000 or your ordinary/special account savings above the Full Retirement Sum :star-struck:") 
            st.warning("You can continue receiving a retirement income no matter what age you live to under CPF LIFE")
if work=="Yes" or avg_wage=="Yes":
    st.write("")
    st.write("") 
    col4,col5 = st.columns(2)
    flat_age = col4.text_input("At what age do you see yourself spending on a house?")
    flat = col4.radio("Do you know how much you will spend on a house?",("Yes (Please enter 0 if you will not be spending)","IDK just use the average housing price for now"))
    
    if flat!="IDK just use the average housing price for now":
        flat_col1,flat_col2 = st.columns(2)
        flat_value = flat_col1.text_input("How much will you spend on your house?")
        if flat_value!=str(0) and flat_value!="":
            percent_of_OA = st.slider("Drag to the percentage of housing cost you would like to use OA on",0,100)
            if percent_of_OA>50:
                st.error("You may have less funds for retirement") 
        elif flat_value=="0":
            percent_of_OA = 0

    if flat=="IDK just use the average housing price for now":
        col5.info("Eh u know ornot? :thinking_face:")
        col5.warning("In 2023, the average amount spent on a house is $400 000")
        flat_value= 400000
        percent_of_OA = st.slider("Drag to the percentage of housing cost you would like to use OA on",0,100)
        if percent_of_OA>50:
            st.error("You may have less funds for retirement")
        
    click=st.button("Click here to see the result!")
    if click:
        try:
            value=cpf_retirement_calculator(int(age), int(salary), int(oa_balance), int(sa_balance), int(ma_balance), int(flat_value), int(percent_of_OA), int(flat_age))
            st.write("")
            st.write("")
            if value[0]<60000:
                st.error("You are not automatically included in CPF Life as you do not have at least $60 000 in your retirement account")
            st.write("Your retirement account will have $", round(value[0]),"by age 65")
            if value[0]>=0 and value[0]>=60000:
                st.write("This means you can get a monthly payout of",round(value[0]/180),"under CPF LIFE!")
            elif value[0]>0 and value[0]<60000:
                st.write("The minimum monthly payout is $350 for non-CPF LIFE members (i.e those enrolled in the Retirement Sum Scheme). You will receive monthly payouts which will stop when your savings run out.")
            else:
                st.write("You are not able to get your monthly payouts :sob:")
            if value[1]==True:
                st.success("Congratulations on hitting the Full Retirement Sum at 55!")
                with st.expander("Click here to understand how you can increase your payouts"):
                    st.warning("The current Full Retirement Sum is $198 800 for the cohort turning 55 in 2023. This is the maximum amount you can have in your special account before you hit 55.")
                    st.warning("When your retirement account is first opened, the maximum amount it has is $198800")
                    st.warning(":bulb: : Once you hit 55, the maximum you can have in your retirement account is increased to the Enhanced Retirement Sum (ERS). The ERS for 2023 is $298800. You can make voluntary top ups to hit the ERS for higher monthly payouts!")
              
            elif value[1]!=True:
                st.success('''Hey there :wave:

Don't be disheartened if this is lower than expected :pensive:

This is why planning early is always useful :smiley:

You can top up to your CPF account starting from today to increase your monthly payouts.

We have done the following calculations for you:''')
                daily_topup= cpf_topup(int(age), int(salary))
                if daily_topup<=0:
                    daily_topup=1
                st.write("You can consider topping up $",math.ceil(daily_topup), "daily from today to reach the full retirement sum by 55")
        except:
            st.error("Please key in all relevant details")
              

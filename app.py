from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import InputRequired, NumberRange


def calc_annuity_payment(loan_amount, loan_term, interest_rate):
    monthly_interest_rate = interest_rate / 1200
    monthly_payment = loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term / (
                (1 + monthly_interest_rate) ** loan_term - 1)
    return round(monthly_payment, 2), round(monthly_payment * loan_term - loan_amount, 2), round(monthly_payment * loan_term, 2)


def calc_diff_payment(loan_amount, loan_term, interest_rate):
    payments = []

    tmp = loan_amount / loan_term
    accrued_interest = 0

    for i in range(loan_term):
        accrued_interest += loan_amount * interest_rate / 1200
        payments.append(tmp + loan_amount * interest_rate / 1200)
        loan_amount -= payments[-1]

    return f"{round(payments[0], 2)}, ..., {round(payments[-1], 2)}", round(accrued_interest, 2), round(sum(payments), 2)


app = Flask(__name__)
app.secret_key = 'any secret string'


class MortgageForm(FlaskForm):
    loan_amount = IntegerField('Сумма кредита (в рублях)', validators=[InputRequired(), NumberRange(1)])
    loan_term = IntegerField('Срок кредита (в месяцах)', validators=[InputRequired(), NumberRange(1)])
    interest_rate = FloatField('Процентная ставка (в год)', validators=[InputRequired(), NumberRange(1)])
    payment_type = SelectField('Тип платежей', choices=[('annuity', 'Аннуитетные'), ('differentiated', 'Дифференцированные')], validators=[InputRequired()])
    submit = SubmitField('Рассчитать')


@app.route('/', methods=['GET', 'POST'])
def mortgage_calculator():
    form = MortgageForm()
    if form.validate_on_submit():
        loan_amount = form.loan_amount.data
        loan_term = form.loan_term.data
        interest_rate = form.interest_rate.data
        payment_type = form.payment_type.data

        result = dict()

        if payment_type == 'annuity':
            result['monthly_payment'], result['accrued_interest'], result['sum_payments'] = calc_annuity_payment(loan_amount, loan_term, interest_rate)
        else:
            result['monthly_payment'], result['accrued_interest'], result['sum_payments'] = calc_diff_payment(loan_amount, loan_term, interest_rate)

        return render_template('result.html', form=form, result=result)

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

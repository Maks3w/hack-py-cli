from decimal import Decimal

from behave import *

from engine.models import Account, Transaction, InvalidTransactionException


@given("an account")
def step_impl(context):
    context.account = Account(1)


@given("the account have deposited {amount:F}")
@when("a deposit of {amount:F} is made")
def step_impl(context, amount: Decimal):
    try:
        context.tx_index += 1
        context.account.tx_add(Transaction.new_deposit(context.account.account_id, context.tx_index, amount))
    except InvalidTransactionException as e:
        context.exception = e


@when("a withdraw of {amount:F} is made")
def step_impl(context, amount: Decimal):
    try:
        context.tx_index += 1
        context.account.tx_add(Transaction.new_withdrawal(context.account.account_id, context.tx_index, amount))
    except InvalidTransactionException as e:
        context.exception = e


@then("the account should have available funds of {available_funds:F}")
def step_impl(context, available_funds: Decimal):
    assert context.account.available_funds == available_funds


@then("the account should have held funds of {held_funds:F}")
def step_impl(context, held_funds: Decimal):
    assert context.account.held_funds == held_funds


@then("the account should have total funds of {total_funds:F}")
def step_impl(context, total_funds: Decimal):
    assert context.account.total_funds == total_funds


@step('a message should be displayed saying "{message}"')
def step_impl(context, message: str):
    assert context.exception is not None, "No error message was raised"
    assert str(context.exception) == message

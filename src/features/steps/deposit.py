from decimal import Decimal

from behave import *

from engine.models import Account, Transaction


@given("an account with available funds of {available_funds:F}")
def step_impl(context, available_funds: Decimal):
    context.account = Account(1)
    context.account.tx_add(Transaction.new_deposit(context.account.account_id, context.tx_index, available_funds))


@when("a deposit of {amount:F} is made")
def step_impl(context, amount: Decimal):
    context.account.tx_add(Transaction.new_deposit(context.account.account_id, context.tx_index, amount))


@then("the available funds should be {available_funds:F}")
def step_impl(context, available_funds: Decimal):
    assert context.account.available_funds == available_funds


@then("the total funds should be {total_funds:F}")
def step_impl(context, total_funds: Decimal):
    assert context.account.total_funds == total_funds

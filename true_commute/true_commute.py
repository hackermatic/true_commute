#!/usr/bin/env python3
# TODO Write a better module-level docstring
"""Calculate your true commute time and cost using an interactive command line.

The user provides their current car commute information using an interactive
command line. This program calculates various metrics about the hidden costs of
that commute and compares them (where possible) to commuting by mass transit,
bicycle, and foot. All of the metrics are displayed to the user including the
"best" commute method for each metric.
"""
import click


class UserCommute(object):
    """Current commute data directly provided by a user.

    All attributes are required.

    Attributes:
        commute_starting_address (str): Any address that can be resolved by
            Google Maps for distance and directions
        commute_ending_address (str): Any address that can be resolved by
            Google Maps for distance and directions
        work_hours_per_week (float)
        wage_per_hour (float): Assumes US dollars
        car_payment_per_month (float): Assumes US dollars
        parking_cost_per_month (float): Assumes US dollars
        is_bike_owner (bool)
    """
    # TODO Switch the money variables to use the money class:
    #     https://pypi.python.org/pypi/money/
    #     (primarily so it's easy to format prettily)
    def __init__(self):
        self.commute_starting_address = None
        self.commute_ending_address = None
        self.work_hours_per_week = None
        self.wage_per_hour = None
        self.car_payment_per_month = None
        self.parking_cost_per_month = None
        self.is_bike_owner = None


def collect_user_commute():
    """Collect user commute data interactively.

    Returns: UserCommute: Populated with valid user data
    """
    user_commute = UserCommute()

    while True:
        # TODO Must use Google Maps API to check start and end locations.
        #      Check at the time of input, validating and reprompting as needed
        #      before continuing to the next attribute.
        user_commute.commute_starting_address = click.prompt(
            "Where does your commute start? (Example: 5505 Farnam St, "
            "Omaha NE 68132)",
            default=user_commute.commute_starting_address, prompt_suffix="\n",
            type=click.STRING)

        user_commute.commute_ending_address = click.prompt(
            "Where does your commute end? (Example: 3555 Farnam St, Omaha NE "
            "68131)",
            default=user_commute.commute_ending_address, prompt_suffix="\n",
            type=click.STRING)

        user_commute.work_hours_per_week = click.prompt(
            "How many hours do you work each week?",
            default=user_commute.work_hours_per_week, prompt_suffix="\n",
            type=click.FLOAT)

        # TODO If a user enters a dollar sign this won't validate
        #     That may be solved when the money class is used instead of float
        user_commute.wage_per_hour = click.prompt(
            "What is your hourly wage (before taxes) in US dollars?",
            default=user_commute.wage_per_hour, prompt_suffix="\n",
            type=click.FLOAT)

        user_commute.car_payment_per_month = click.prompt(
            "What do you spend on car loans and leases each month?",
            default=user_commute.car_payment_per_month, prompt_suffix="\n",
            type=click.FLOAT)

        user_commute.parking_cost_per_month = click.prompt(
            "What do you spend on parking each month?",
            default=user_commute.parking_cost_per_month, prompt_suffix="\n",
            type=click.FLOAT)

        user_commute.is_bike_owner = click.confirm(
            "Do you own a bike?",
            default=user_commute.is_bike_owner, prompt_suffix="\n")

        if not click.confirm("Do you need to correct any answers?"):
            break

    return user_commute


def cli():
    """Command-line program interface
    """
    # TODO Display a welcome banner and basic instructions
    user_commute = collect_user_commute()
    # TODO Now the hard stuff!

if __name__ == "__main__":
    cli()

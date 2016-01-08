#!/usr/bin/env python3
"""true_commute: Calculate your true commute time and cost
"""
import click


class UserCommute(object):
    """Current commute data directly provided by a user
    """
    def __init__(self):
        self.start_location = None
        self.end_location = None
        self.work_hours_per_week = None
        self.wage_per_hour = None
        self.car_payment_per_month = None
        self.parking_cost_per_month = None
        self.bike_owner = None


def collect_user_commute():
    """Collect user commute data interactively
    """
    commute = UserCommute()

    while True:
        # TODO Must use Google Maps API to check start and end locations,
        # then reprompt for them as needed
        commute.start_location = click.prompt(
            "Where does your commute start?",
            default=commute.start_location or "5505 Farnam St, Omaha NE 68132",
            prompt_suffix=" ", type=click.STRING)

        commute.end_location = click.prompt(
            "Where does your commute end?",
            default=commute.end_location or "3555 Farnam St, Omaha NE 68131",
            prompt_suffix=" ", type=click.STRING)

        commute.work_hours_per_week = click.prompt(
            "How many hours do you work each week?",
            default=commute.work_hours_per_week or 20,
            prompt_suffix=" ", type=click.INT)

        # TODO Should format the [default] dollar values to $x.yy somehow
        commute.wage_per_hour = click.prompt(
            "What is your hourly wage (before taxes) in US dollars?",
            default=commute.wage_per_hour or 7.25,
            prompt_suffix=" ", type=click.FLOAT)

        commute.car_payment_per_month = click.prompt(
            "What do you spend on car loans and leases each month?",
            default=commute.car_payment_per_month or 0,
            prompt_suffix=" ", type=click.FLOAT)

        commute.parking_cost_per_month = click.prompt(
            "What do you spend on parking each month?",
            default=commute.parking_cost_per_month or 0,
            prompt_suffix=" ", type=click.FLOAT)

        commute.bike_owner = click.confirm(
            "Do you own a bike?",
            default=commute.bike_owner or False,
            prompt_suffix=" ")

        if not click.confirm("Do you need to correct any answers?"):
            break

    return commute


def cli():
    """Command-line program interface
    """
    commute = collect_user_commute()
    # TODO Now the hard stuff!

if __name__ == "__main__":
    cli()

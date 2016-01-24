#!/usr/bin/env python3
"""Calculate your true commute time and cost using an interactive command line.

The user provides their current car commute information using an interactive
command line. This program calculates and displays various metrics about the
hidden costs of that commute.

This module requires a Google API key, which you can obtain from
<https://console.developers.google.com>. Set it as an environment variable
named ``GOOGLE_API_KEY``.

Attributes:
    CLI_PROMPT_SUFFIX (str): Appended to each ``click`` prompt
    MAPS_CLIENT (googlemaps.client.Client): Geocodes user input and obtains
        directions

Raises:
    KeyError: If the environment variable ``GOOGLE_API_KEY`` is not set
"""
import os
import sys

import click
from googlemaps import client, geocoding, distance_matrix

# TODO Decorate(?)/wrap the click functions to apply this suffix automatically
CLI_PROMPT_SUFFIX = "\n"

# TODO Is there a way to group the __main__ handling in the main block?
# TODO Determine a reasonable Maps timeout; default is no per-request timeout
#      and 60 seconds total for retriable requests
# TODO Also support the client key and ID pair
try:
    # TODO Should I uppercase this variable name?
    MAPS_CLIENT = client.Client(key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    if __name__ == "__main__":
        sys.stderr.write("Please set the environment variable GOOGLE_API_KEY")
        sys.exit(1)
    raise


class UserCommute(object):
    """Current commute data directly provided by a user.

    All attributes are required.

    Attributes:
        commute_starting_address (str): Any address that can be geocoded by
            Google Maps for distance and directions
        commute_ending_address (str): Any address that can be geocoded by
            Google Maps for distance and directions
        work_days_per_week (int)
        work_hours_per_week (float)
        wage_per_hour (float): Assumes US dollars
        car_payment_per_month (float): Assumes US dollars
        parking_cost_per_month (float): Assumes US dollars
    """
    # TODO Switch the money variables to use the money class:
    #     https://pypi.python.org/pypi/money/
    #     (primarily so it's easy to format prettily)
    def __init__(
            self, commute_starting_address=None, commute_ending_address=None,
            work_days_per_week=None, work_hours_per_week=None,
            wage_per_hour=None, car_payment_per_month=None,
            parking_cost_per_month=None):
        self.commute_starting_address = commute_starting_address
        self.commute_ending_address = commute_ending_address
        self.work_days_per_week = work_days_per_week
        self.work_hours_per_week = work_hours_per_week
        self.wage_per_hour = wage_per_hour
        self.car_payment_per_month = car_payment_per_month
        self.parking_cost_per_month = parking_cost_per_month


def collect_user_commute():
    """Collect user commute data interactively.

    This function performs basic input validation and prompts the user to
    confirm all values before returning.

    Returns:
         UserCommute: Populated with valid user data
    """
    user_commute = UserCommute()

    while True:
        user_commute.commute_starting_address = _collect_geocoded_address(
            "Where does your commute start? (Example: 5505 Farnam St, "
            "Omaha NE 68132)", default=user_commute.commute_starting_address)

        user_commute.commute_ending_address = _collect_geocoded_address(
            "Where does your commute end? (Example: 3555 Farnam St, Omaha NE "
            "68131)", default=user_commute.commute_ending_address)

        user_commute.work_days_per_week = click.prompt(
            "How many days do you work each week?",
            default=user_commute.work_days_per_week,
            prompt_suffix=CLI_PROMPT_SUFFIX, type=click.INT)

        user_commute.work_hours_per_week = click.prompt(
            "How many hours do you work each week?",
            default=user_commute.work_hours_per_week,
            prompt_suffix=CLI_PROMPT_SUFFIX, type=click.FLOAT)

        # TODO If a user enters a dollar sign this won't validate
        #     That may be solved when the money class is used instead of float
        user_commute.wage_per_hour = click.prompt(
            "What is your hourly wage (before taxes) in US dollars?",
            default=user_commute.wage_per_hour,
            prompt_suffix=CLI_PROMPT_SUFFIX, type=click.FLOAT)

        user_commute.car_payment_per_month = click.prompt(
            "What do you spend on car loans and leases each month?",
            default=user_commute.car_payment_per_month,
            prompt_suffix=CLI_PROMPT_SUFFIX, type=click.FLOAT)

        user_commute.parking_cost_per_month = click.prompt(
            "What do you spend on parking each month?",
            default=user_commute.parking_cost_per_month,
            prompt_suffix=CLI_PROMPT_SUFFIX, type=click.FLOAT)

        if not click.confirm("Do you need to correct any answers?"):
            break

    return user_commute


def _collect_geocoded_address(text, default=None):
    """Collect user address data interactively.

    This function geocodes user input using Google Maps and prompts the user to
    confirm the geocoded address before returning. The user is prompted to
    try again when there are zero or multiple geocoding candidates.

    Arguments:
        text: The text to show for the prompt

    Returns:
         str: The formatted_address from a Google Maps geocode operation
    """
    while True:
        user_address = click.prompt(
                text, default=default, prompt_suffix=CLI_PROMPT_SUFFIX,
                type=click.STRING)

        geocoded = geocoding.geocode(MAPS_CLIENT, user_address)
        if len(geocoded) == 0:
            print("Google Maps can't find that address. Please be more "
                  "specific.")
        elif len(geocoded) > 1:
            # TODO List up to three of the results
            print("Google Maps found multiple results with that address. "
                  "Please be more specific.")
        elif "partial_match" in geocoded[0]:
            print(
                    "Google Maps found a partial match: " +
                    geocoded[0]["formatted_address"] + ". Please be more "
                    "specific.")
        else:
            formatted_address = geocoded[0]["formatted_address"]
            if click.confirm(
                    "Is the correct address " + formatted_address + "?",
                    prompt_suffix=CLI_PROMPT_SUFFIX, default=True):
                return formatted_address


def get_commute_details(commute_starting_address, commute_ending_address):
    """Get commute time and distance from Google Maps

    Arguments:
        commute_starting_address (str): Any address that can be geocoded by
            Google Maps for distance and directions. Where possible, store the
            ``formatted_address`` from a Google Maps geocode operation.
        commute_ending_address (str): Any address that can be geocoded by
            Google Maps for distance and directions. Where possible, store the
            ``formatted_address`` from a Google Maps geocode operation.

    Returns:
         dict: ``{"duration_seconds": int, "distance_meters": int}`` or None if
         Google Maps can't create directions for these addresses.
    """
    api_result = distance_matrix.distance_matrix(
            MAPS_CLIENT, commute_starting_address, commute_ending_address)
    api_result = api_result['rows'][0]['elements'][0]

    if api_result['status'] != "OK":
        return None

    return {"duration_seconds": api_result['duration']['value'],
            "distance_meters": api_result['distance']['value']}


def cli():
    """Command-line program interface
    """
    # TODO Display a welcome banner and basic instructions
    user_commute = collect_user_commute()
    details = get_commute_details(
            user_commute.commute_starting_address,
            user_commute.commute_ending_address)
    # TODO Now the hard stuff!


if __name__ == "__main__":
    cli()

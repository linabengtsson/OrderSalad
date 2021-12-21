import datetime


class Salad:
    """Attributes:
    salad: A string with the salad the customer wants
    ingredients: A list with the ingredients the salads contains
    price: An float with the price of the salad
    """

    def __init__(self, salad, ingredients, price):
        """
        Creates a new salad.
        """
        self.salad = salad
        self.ingredients = ingredients
        self.price = int(price)
        self.adding_ingredients = []
        self.compare_set = []

    def __str__(self):
        """
        :return: A string with information about the salad and its price.
        """
        return self.salad + ", " + str(self.price) + " dollar, contains the ingredients: " + str(self.ingredients) + "."

    def change_cost(self, price_of_ingredient):
        """
        Changes the total cost after adding the price of a new ingredient.
        :return: A float with the new price
        """
        self.price += int(price_of_ingredient)

    def add_ingredients(self, extra_ingredients):
        """
        Changes the list of ingredients of the salad.
        :param extra_ingredients: A list of the ingredient/s that the customer wants to add.
        :return: An updated list of the ingredients.
        """
        for ingredient in extra_ingredients:
            self.ingredients.append(ingredient)


def get_int_input(prompt_string):
    """
    Used to get an int from the customer and asks again if the customer writes something else
    :param prompt_string: A string that explains for the customer what to input.
    :return: The int the customer chose.
    """
    int_value = 0
    done = False
    while not done:
        try:
            int_value = int(input(prompt_string))
        except ValueError:
            print("Try with a number instead!")
        else:
            done = True
    return int_value


def create_list_of_ingredients(file_name):
    """
    Creates a list of ingredients and thier prices.
    :param file_name: The file to get the ingredients and prices from
    :return: A list of ingredients and their prices
    """
    file = open(file_name, "r")
    empty_list = file.readlines()
    ingredient_list = []
    for line in empty_list:
        line = line.strip()
        ingredient_list.append(line.split(","))
    file.close()
    return ingredient_list


def menu(ingredient_list):
    """
    Welcomes the customer and creates a menu from the list in create_list_of_ingredients().
    :param ingredient_list: A list of ingredients and their prices
    :return: All the ingredients in form of a menu with numbers in front of each ingredient.
    """
    number = 0
    print("""\nHello and welcome to "Calle at the Corner"! \N{grinning face}\n
Choose the ingredients you want in your salad.""")
    for index, item in ingredient_list:
        number += 1
        print(str(number) + ": " + index)


def yes_or_no(prompt_string):
    """
    A function to use when the customer is supposed to answer yes or no.
    :param prompt_string: A question the customer answers to
    :return: True or False
    """
    while True:
        try:
            yes_no = input(prompt_string)
            yes = ["Yes", "yes", "y"]
            no = ["No", "no", "n"]
            if yes_no in yes:
                return True
            elif yes_no in no:
                return False
            else:
                raise ValueError("You need to answer yes or no.")
        except ValueError as error:
            print(error)


def menu_choice():
    """
    Asks what the customer wants in he's salad in form of numbers.
    :return: All the made choices in form of numbers in a list.
    """
    choice_list = []
    while True:
        try:
            choice = get_int_input("\nWhat ingredient do you want in your salad? Pick a number! (Just ONE number)")
            if choice not in range(1, 7):
                raise ValueError
            if choice in choice_list:
                print("You have already chosen that ingredient.")
            else:
                choice_list.append(choice)
                yon = yes_or_no("Do you want to add another ingredient? Yes or no?")
                if yon is True:
                    continue
                else:
                    break
        except ValueError:
            print("You need to choose a number between 1 and 6.")
    return choice_list


def new_salad(file_name):
    """
    Creates new salads from the file "Salads".
    :param file_name: The file to get the salads
    :return: A list of all the Salad objects
    """
    file = open(file_name, "r")
    get_salad_list = file.readlines()  # Delar upp varje rad i filen till listor
    salad_list = []
    for content in get_salad_list:
        new_content = content.split(".")
        name = new_content[0]
        price = new_content[1]
        ingredients = new_content[2:-1]
        salad_list.append(Salad(name, ingredients, price))
    file.close()
    return salad_list


def choices_in_list_with_strings(choice_list, ingredient_list):
    """
    Takes the list that man_choice() creates and redo all the numbers into the string it represent by comparing
    the list and the list with ingredients and their prices.
    :param choice_list: List with all the wanted ingredients in form of numbers
    :param ingredient_list: List with all ingredients and their prices
    :return: A list with the ingredients the customer wants in form of strings
    """
    choice_string_list = []
    for i in range(len(choice_list)):
        choice_string_list.append(ingredient_list[choice_list[i] - 1][0])
    print("You have chosen: " + str(choice_string_list) + "\n")
    return choice_string_list


def compare_numbers_of_hits(choice_string_list, salad_list):
    """
    Compares the inputs with the Salad-objects and checks if all the ingredients exist in the same salad. Also remakes
    list with the ingredients the customer wants into a set. Makes a list of the salad objects that matches perfectly.
    :param choice_string_list: A list with the ingredients the customer wants in form of strings.
    :param salad_list: A list of all the Salad objects
    :return: Numbers of salads that matches perfectly, set of the ingredients the customer wants and list of salad
    objects that matches perfectly.
    """
    compare_set = set(choice_string_list)
    salads_containing_all_ingredients = 0
    matching_salads = []

    for salad in salad_list:
        value_number_ingredients = 0
        for ingredient in compare_set:
            if ingredient in salad.ingredients:
                value_number_ingredients += 1
        if value_number_ingredients == len(compare_set):
            salads_containing_all_ingredients += 1
            matching_salads.append(salad)
    return salads_containing_all_ingredients, compare_set, matching_salads


def getting_cheapest_salad(matching_salads):
    """
    This function is used when there are several salads that matches the customers wishes and choe the cheapest
    of them.
    :param matching_salads: A list with all the salad objects that matches the customers wishes.
    :return: The salad object that is the cheapest.
    """
    perfect_match = Salad("", [], 0)
    prices_salads = {}
    for salad in matching_salads:
        prices_salads[salad.salad] = salad.price
    best_salad = min(prices_salads, key=prices_salads.get)
    for salad in matching_salads:
        if salad.salad == best_salad:
            perfect_match = salad
    print(perfect_match)
    return perfect_match


def missing_ingredient_from_choice(compare_set, perfect_match):
    """
    Finds out which ingredient that does not exist in the salad that was suggested when there were no perfect
    match of salad. Also tells the customer that he can add this ingredient later on.
    :param compare_set: A set of the ingredients the customer wants.
    :param perfect_match: The salad that contains most ingredients that the customer wanted and is also the
    cheapest.
    :return: The salad that contains most ingredients that the customer wanted and is also the cheapest.
    """
    missing_ingredient = compare_set.difference(set(perfect_match.ingredients))
    print("You had also chosen: {} which is not part of the {}. \nYou will be able to add {} later to your salad.".
          format(missing_ingredient, perfect_match.salad, missing_ingredient))
    return perfect_match


def zero_matching_salads(salad_list, compare_set):
    """
    This function is used when there are no salad that matches perfectly with the wanted ingredients. It searches
    for the salad with most common ingredients and the cheapest one.
    :param salad_list: A list with all the salad objects.
    :param compare_set: A set of the ingredients the customer wants.
    :return: The salad that contains most ingredients that the customer wanted and is also the
    cheapest.
    """
    perfect_match = Salad("", [], 0)
    max_length = 0
    perfect_salads_list = []
    prices_salads = {}
    for salad in salad_list:
        comparing = compare_set.intersection(salad.ingredients)
        if len(comparing) > max_length:
            max_length = len(comparing)
            perfect_match = salad
            perfect_salads_list.append(salad)
            if len(perfect_salads_list) > 1:
                del perfect_salads_list[1:]
        elif len(comparing) == max_length:
            perfect_salads_list.append(salad)
            for element in perfect_salads_list:
                prices_salads[element.salad] = element.price
            best_salad = min(prices_salads, key=prices_salads.get)
            for element in perfect_salads_list:
                if element.salad == best_salad:
                    perfect_match = element
    print(perfect_match)
    return perfect_match


def compare(salads_containing_all_ingredients, compare_set, matching_salads, salad_list):
    """
    This function handles several things. It checks how many salads that matches the customers wishes perfectly and
    then bring out the perfect salad.
    :param salads_containing_all_ingredients: A number of how many salads that contains all the ingredients.
    :param compare_set: A set of the ingredients the customer wants.
    :param matching_salads: A list with all the salad objects that matches the customers wishes.
    :param salad_list: A list with all the salad objects.
    :return: The final salad that matches the best with what the customer wanted.
    """
    if salads_containing_all_ingredients == 0:
        print("You got zero perfect matches, so we present the cheapest with most common ingredients as you desired:")
        return missing_ingredient_from_choice(compare_set, zero_matching_salads(salad_list, compare_set))

    elif salads_containing_all_ingredients == 1:
        print("PERFECT MATCH! The salad that matches your wishes:")
        perfect_match = Salad("", [], 0)
        for salad in matching_salads:
            perfect_match = salad
        print(perfect_match)
        return perfect_match

    elif salads_containing_all_ingredients >= 2:
        print("You got two or more matches, so we present the cheapest:")
        return getting_cheapest_salad(matching_salads)


def happy():
    """
    Asks if the customer is happy. If the customer is happy with his salad the function will get True. If the customer
    is not happy, the function will get False.
    :return: True or False
    """
    yon = yes_or_no("\nAre you satisfied with the proposed salad? Yes or no? ('No' takes you back to the start)")
    return yon


def add_ingredients(ingredient_list):
    """
    Shows a menu containing all ingredients and their prices.
    :param ingredient_list: A list of ingredients and their prices.
    :return: A menu of all the ingredients and their prices with numbers in front of each ingredients.
    """
    number = 0
    print("\nNow you will be able to upgrade your salad by adding some nice ingredients!")
    for index, item in ingredient_list:
        number += 1
        print(str(number) + ": " + index + ", " + item + " dollar.")


def add_ingredients_choice(perfect_match, ingredient_list):
    """
    Asks if the customer wants to add some ingredients. If yes, asks the customer which ingredients he wants. Then
    adds the ingredients and the price to the salad.
    :param perfect_match: The salad that matches best with what the customer wants.
    :param ingredient_list: A list of all ingredients and their prices.
    :return: The updated salad object
    """
    yon = yes_or_no("\nDo you want to add some ingredients? Yes or no?")
    if yon:
        extra_ingredients = choices_in_list_with_strings(menu_choice(), ingredient_list)
        salad = perfect_match
        salad.add_ingredients(extra_ingredients)
        for e in range(len(ingredient_list)):
            for i in range(len(extra_ingredients)):
                if ingredient_list[e][0] == extra_ingredients[i]:
                    price = ingredient_list[e][1]
                    salad.change_cost(price)
        print("The ingredients have successfully been added to your salad. Your salad has now a new look:")
        print(perfect_match)
    return perfect_match


def receipt(file_name, perfect_match):
    """
    Creates a file and write about the purchase in it.
    :param file_name: The file where to write the receipt.
    :param perfect_match: The salad object that the customer wants to buy, the perfect match
    :return: A receipt on a new file.
    """
    file = open(file_name, "w")
    date_time = datetime.datetime.now()
    name = input("\nWhat's your name?")
    file.write("""Thanks {} for your pursuit at "Calle at the corner".\n\nYou have ordered:\n{}\n\nDate: {}\n
Have a nice day!""".format(name, perfect_match, date_time))
    file.close()


def main():
    while True:
        list_ing = create_list_of_ingredients("Ingredients.txt")
        menu(list_ing)
        salad_object = new_salad("Salads.txt")
        hits = compare_numbers_of_hits(choices_in_list_with_strings(menu_choice(), list_ing), salad_object)
        comparing = compare(hits[0], hits[1], hits[2], salad_object)
        add_ingredients(list_ing)
        aic = add_ingredients_choice(comparing, list_ing)
        if not happy():
            print("Okey, now you will be able to choose a new salad!")
            main()
        receipt("Receipt.txt", aic)
        break


if __name__ == "__main__":
    main()

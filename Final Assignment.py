import tkinter as tk
import tkinter.messagebox as messagebox
import datetime
import pickle
from enum import Enum

class TicketType(Enum):
    SINGLE_DAY_PASS = {
        "description": "Access to the park for one day.",
        "limitations": "Valid only on selected date.",
        "validity": "1 day",
        "discount_available": "None",
    }
    TWO_DAY_PASS = {
        "description": "Access to the park for two consecutive days.",
        "limitations": "Cannot be split over multiple trips.",
        "validity": "2 days",
        "discount_available": "10% discount for online purchase.",
    }
    ANNUAL_MEMBERSHIP = {
        "description": "Unlimited access for one year.",
        "limitations": "Must be used by the same person",
        "validity": "1 year",
        "discount_available": "15% discount on renewal.",
    }
    CHILD_TICKET = {
        "description": "Discounted ticket for children age (3-12)",
        "limitations": "Valid only on selected date must be accompanied by an adult.",
        "validity": "1 day",
        "discount_available": "None.",
    }
    GROUP_TICKET = {
        "description": "Special rate for groups of 10",
        "limitations": "Must be booked in advance.",
        "validity": "1 day",
        "discount_available": "20% off for groups of 20 or more.",
    }
    VIP_EXPERIENCE_PASS = {
        "description": "Includes expedited access and reserved seating for shows",
        "limitations": "Limited availability must be purchased in advance.",
        "validity": "1 day",
        "discount_available": "None.",
    }

class TicketBookingSystem:
    def __init__(self):
        self.__guests = []  # List of Guest objects
        self.__admin = None           # Admin object
        self.__events = []
        self.__total_sales = 0

    # Getters and Setters
    def get_registered_guests(self):
        return self.__guests

    def set_guests(self, guests):
        if isinstance(guests, list):
            self.__guests = guests
        else:
            raise TypeError("Guests should be a list.")

    def get_admin(self):
        return self.__admin

    def set_admin(self, admin):
        self.__admin = admin

    def get_events(self):
        return self.__events

    def set_events(self, events):
        if isinstance(events, list):
            self.__events = events
        else:
            raise TypeError("Events should be a list.")

    def get_total_sales(self):
        return self.__total_sales

    def set_total_sales(self, total_sales):
        if isinstance(total_sales, (int, float)):
            self.__total_sales = total_sales
        else:
            raise TypeError("Total sales should be a number.")

    def increase_total_sales(self, amount):
        """Increases the total sales by a given amount."""
        if isinstance(amount, (int, float)) and amount > 0:
            self.__total_sales += amount
        else:
            raise ValueError("Amount should be a positive number.")

    def register_new_guest(self, new_guest):
        """Adding a new guest to the system."""
        self.__guests.append(new_guest)

    def delete_guest(self, guest_id):
        """Deleting a guest from the system by their ID."""

        for guest in self.__guests:
            if guest.get_guest_id() == guest_id:
                self.__guests.remove(guest)
                return True

        return False

    def fetch_guest_by_id(self, id):
        '''
        Returns a guest by the id
        '''
        for g in self.__guests:
            if g.get_guest_id() == id:
                return g

        return False

    def fetch_guest_by_name(self, name):
        """
        Returns a guest by name
        """
        for g in self.__guests:
            if g.get_name().lower() == name.lower():  # Case-insensitive match
                return g
        return None  # Explicitly return None when no guest is found

    def create_event(self, name, start_date, end_date):
        '''
        Creates event and adds it into the system
        '''
        event = Event(name, start_date, end_date)
        self.__events.append(event)

    def fetch_guest_purchase_history(self, guest_name):
        """
        Returns the purchase history for the guest
        """
        guest = self.fetch_guest_by_name(guest_name)
        if not guest:  # Check if the guest was not found
            return f"No guest found with the name '{guest_name}'."
        return guest.purchase_history()

    def get_tickets(self):
        return [
            Ticket(1, 275, "", TicketType.SINGLE_DAY_PASS),
            Ticket(2, 480, "", TicketType.TWO_DAY_PASS),
            Ticket(3, 1840, "", TicketType.ANNUAL_MEMBERSHIP),
            Ticket(4, 185, "", TicketType.CHILD_TICKET),
            Ticket(5, 220, "", TicketType.GROUP_TICKET),
            Ticket(6, 550, "", TicketType.VIP_EXPERIENCE_PASS),
        ]

    def create_event(self, name, start_date, end_date):
        event = Event(name, start_date, end_date, self)  # Binary association
        self.__events.append(event)

class Event:
    def __init__(self, name, start_date, end_date, system: TicketBookingSystem):
        self.__name = name
        self.__start_date = start_date
        self.__end_date = end_date
        self.__system = system  # Binary association
        self.__save_to_file()
        self.save_to_text_file()

    def save_to_text_file(self):
        """Save event details to a .txt file."""
        file_name = f"event_{self.__name.replace(' ', '_')}.txt"
        with open(file_name, "w") as file:
            file.write(f"Event Name: {self.__name}\n")
            file.write(f"Start Date: {self.__start_date}\n")
            file.write(f"End Date: {self.__end_date}\n")

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_start_date(self):
        return self.__start_date

    def set_start_date(self, start_date):
        self.__start_date = start_date

    def get_end_date(self):
        return self.__end_date

    def set_end_date(self, end_date):
        self.__end_date = end_date

    def get_system(self):
        return self.__system

    def set_system(self, system):
        self.__system = system

    def __save_to_file(self):
        """
        Saves the object into a pickle file.
        """
        events = self.load_events()  # Load existing events
        if self not in events:  # Check for duplicate
            events.append(self)  # Add new event
            with open("events.pkl", "wb") as file:
                pickle.dump(events, file)

    def load_events(self):
        """
        Loads all events from a pickle file if it exists.
        """
        try:
            with open("events.pkl", "rb") as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            return []


class User:
    def __init__(self, name, email, password):
        self.__name = name
        self.__email = email
        self.__password = password

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password

class Guest(User):
    def __init__(self, guest_id, name, email, password, phone, system: TicketBookingSystem):
        super().__init__(name, email, password)
        self.__guest_id = guest_id
        self.__phone = phone
        self.__purchase_orders = []
        self.__bookingsystem = system  # Aggregation

        # Save guest data to a .txt file
        self.save_to_text_file()

        # Load existing guests and save this guest to file
        guests = self.load_guests()
        for x, guest in enumerate(guests):
            if guest.get_guest_id() == self.__guest_id:
                guests[x] = self  # Update existing guest
                break
        else:
            guests.append(self)  # Add new guest

        self.save_guests_to_file(guests)

    def save_to_text_file(self):
        """Save guest details to a .txt file."""
        file_name = f"guest_{self.__guest_id}.txt"
        with open(file_name, "w") as file:
            file.write(f"Guest ID: {self.__guest_id}\n")
            file.write(f"Name: {self.get_name()}\n")
            file.write(f"Email: {self.get_email()}\n")
            file.write(f"Phone: {self.__phone}\n")

    def get_guest_id(self):
        return self.__guest_id

    def set_guest_id(self, guest_id):
        self.__guest_id = guest_id

    def get_phone(self):
        return self.__phone

    def set_phone(self, phone):
        self.__phone = phone

    def get_purchase_orders(self):
        return self.__purchase_orders

    def set_purchase_orders(self, purchase_orders):
        self.__purchase_orders = purchase_orders

    def add_purchase_order(self, order_id, tickets, total_price):
        purchase_order = PurchaseOrder(order_id, tickets, total_price, datetime.datetime.now())  # Composition
        self.__purchase_orders.append(purchase_order)

    def purchase_history(self):
        """Return a string representation of the guest's purchase history."""
        if not self.__purchase_orders:
            return "No purchase history available."

        history = f"Purchase History for {self.get_name()}:\n"
        history += "=" * 40 + "\n"

        for order in self.__purchase_orders:
            history += f"Order ID: {order.get_order_id()}\n"
            history += f"Order Date: {order.get_order_date()}\n"
            history += f"Total Price: DHS{order.get_total_price():}\n"
            history += "Tickets:\n"

            for ticket in order.get_tickets():
                history += (
                    f"  - Ticket ID: {ticket.get_ticket_id()}\n"
                    f"    Description: {ticket.get_description()}\n"
                    f"    Price: DHS{ticket.get_price():}\n"
                    f"    Visit Date: {ticket.get_visit_date()}\n"
                    f"    Limitations: {ticket.get_limitations()}\n"
                    f"    Validity: {ticket.get_validity()} days\n"
                    f"    Discount Available: {ticket.get_discount_available()}\n"
                )
            history += "-" * 40 + "\n"

        return history

    def save_guests_to_file(self, guests):
        """Save the list of guests to a file."""
        with open("guests.pkl", "wb") as file:
            pickle.dump(guests, file)

    def load_guests(self):
        """Load the list of guests from a file."""
        try:
            with open("guests.pkl", "rb") as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            return []


class PurchaseOrder:
    def __init__(self, order_id, tickets, total_price, order_date):
        self.__order_id = order_id
        self.__tickets = tickets  # Directly use the list of Ticket objects
        self.__total_price = total_price
        self.__order_date = order_date
        self.__save_to_file()

    def get_order_id(self):
        return self.__order_id

    def set_order_id(self, order_id):
        self.__order_id = order_id

    def get_tickets(self):
        return self.__tickets  # List of Ticket objects

    def set_tickets(self, tickets):
        self.__tickets = tickets

    def get_total_price(self):
        return self.__total_price

    def set_total_price(self, total_price):
        self.__total_price = total_price

    def get_order_date(self):
        return self.__order_date

    def set_order_date(self, order_date):
        self.__order_date = order_date

    def __save_to_file(self):
        """
        Saves the purchase order object into a pickle file.
        """
        orders = self.load_orders()
        for x, order in enumerate(orders):
            if order.get_order_id() == self.__order_id:
                orders[x] = self  # Update existing order
                break
        else:
            orders.append(self)  # Add new order

        with open("purchase_orders.pkl", "wb") as file:
            pickle.dump(orders, file)

    def load_orders(self):
        """
        Loads all orders from a pickle file if it exists.
        """
        try:
            with open("purchase_orders.pkl", "rb") as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            return []

class Ticket:
    def __init__(self, ticket_id, price, visit_date, ticket_type: TicketType):
        if not isinstance(ticket_type, TicketType):
            raise ValueError(f"Invalid ticket type: {ticket_type}")
        self.__ticket_id = ticket_id
        self.__price = price
        self.__visit_date = visit_date
        self.__ticket_type = ticket_type
        self.__description = ticket_type.value["description"]
        self.__limitations = ticket_type.value["limitations"]
        self.__validity = ticket_type.value["validity"]
        self.__discount_available = ticket_type.value["discount_available"]

    def get_ticket_id(self):
        return self.__ticket_id

    def set_ticket_id(self, ticket_id):
        self.__ticket_id = ticket_id

    def get_price(self):
        # Adjust price for group ticket
        return self.__price * 10 if self.__ticket_type == TicketType.GROUP_TICKET else self.__price

    def set_price(self, price):
        self.__price = price

    def get_visit_date(self):
        return self.__visit_date

    def set_visit_date(self, visit_date):
        self.__visit_date = visit_date

    def get_ticket_type(self):
        return self.__ticket_type.name  # Return name of the Enum

    def set_ticket_type(self, ticket_type):
        self.__ticket_type = ticket_type

    def get_description(self):
        return self.__description

    def set_description(self, description):
        self.__description = description

    def get_limitations(self):
        return self.__limitations

    def set_limitations(self, limitations):
        self.__limitations = limitations

    def get_validity(self):
        return self.__validity

    def set_validity(self, validity):
        self.__validity = validity

    def get_discount_available(self):
        return self.__discount_available

    def set_discount_available(self, discount_available):
        self.__discount_available = discount_available

class Admin(User):
    def __init__(self, admin_id, name, email, password, system: TicketBookingSystem):
        super().__init__(name, email, password)
        self.__admin_id = admin_id
        self.__bookingsystem = system  # Aggregation

    def get_admin_id(self):
        return self.__admin_id

    def set_admin_id(self, admin_id):
        self.__admin_id = admin_id

    def manage_system(self):
        # Example of admin interacting with the TicketBookingSystem
        return f"Managing system with total sales: {self.__bookingsystem.get_total_sales()}"

ticket_auto_id = 0

# Creating objects
system = TicketBookingSystem()

# Create Admin instance with reference to the system (Aggregation relationship)
admin = Admin("Admin", "Khalifa", "Khalifa123@gmail.com", "khalifa123", system)

# Create Guest instances with reference to the system (Aggregation relationship)
guest_1 = Guest(1, "Abdulla", "Abdulla_Alremeithi@gmail.com", "2837003", "0501234567", system)
system.register_new_guest(guest_1)

guest_2 = Guest(2, "Bu Khalfan", "Bu_Khalfan@gmail.com", "8726384", "0503456789", system)
system.register_new_guest(guest_2)

guest_3 = Guest(3, "Afshan", "Afshan@gmail.com", "23894682", "0509876543", system)
system.register_new_guest(guest_3)

# Create Events associated with the system (Binary relationship)
system.create_event("National Day", "2/12/2024", "3/12/2024")
system.create_event("Your Voice Campaign", "16/11/2024", "17/11/2024")
system.create_event("Emirati Women's Day", "1/11/2024", "2/11/2024")
system.create_event("Flag Day", "3/11/2024", "4/11/2024")

# Discount criteria for tickets (additional customization)
single_day_pass_discount = "None"
two_day_pass_discount = "10% discount for online purchase."
annual_membership_discount = "15% discount on renewal."
child_ticket_discount = "None."
group_ticket_discount = "20% off for groups of 20 or more."
vip_experience_discount = "None."


def open_registration_window():
    reg_window = tk.Toplevel(root)
    reg_window.title("Registration Window")
    reg_window.geometry("400x400")
    reg_window.configure(bg="#FFE4C4")

    reg_label = tk.Label(
        reg_window,
        text="Register a New Guest",
        font=("Times", 16, "bold"),
        bg="#FFE4C4",
        fg="#4B4B4B",
    )
    reg_label.pack(pady=20)

    id_label = tk.Label(reg_window, text="Guest ID:", font=(
        "Times", 12), bg="#FFE4C4", fg="#4B4B4B")
    id_label.pack(anchor="w", padx=40, pady=5)
    id_entry = tk.Entry(reg_window, font=("Times", 12), width=30)
    id_entry.pack(padx=40, pady=5)

    name_label = tk.Label(reg_window, text="Name:", font=(
        "Times", 12), bg="#FFE4C4", fg="#4B4B4B")
    name_label.pack(anchor="w", padx=40, pady=5)
    name_entry = tk.Entry(reg_window, font=("Times", 12), width=30)
    name_entry.pack(padx=40, pady=5)

    email_label = tk.Label(reg_window, text="Email:", font=(
        "Times", 12), bg="#FFE4C4", fg="#4B4B4B")
    email_label.pack(anchor="w", padx=40, pady=5)
    email_entry = tk.Entry(reg_window, font=("Times", 12), width=30)
    email_entry.pack(padx=40, pady=5)

    phone_label = tk.Label(reg_window, text="Phone Number:", font=(
        "Times", 12), bg="#FFE4C4", fg="#4B4B4B")
    phone_label.pack(anchor="w", padx=40, pady=5)
    phone_entry = tk.Entry(reg_window, font=("Times", 12), width=30)
    phone_entry.pack(padx=40, pady=5)

    def submit_registration():
        guest_id = id_entry.get()
        name = name_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()

        if not guest_id or not name or not email or not phone:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Default password for new guests (you can improve this)
        default_password = "password123"

        # Create the Guest object with all required parameters
        guest = Guest(guest_id, name, email, default_password, phone, system)
        system.register_new_guest(guest)

        messagebox.showinfo(
            "Success", f"Guest Registered:\n\nName: {name}\nEmail: {email}\nPhone: {phone}"
        )
        reg_window.destroy()

    submit_button = tk.Button(
        reg_window,
        text="Submit",
        font=("Times", 12, "bold"),
        bg="#008CBA",
        fg="white",
        width=15,
        command=submit_registration,
    )
    submit_button.pack(pady=20)


def open_delete_guest_window():
    delete_window = tk.Toplevel(root)
    delete_window.title("Guest Delete Window")
    delete_window.geometry("400x400")
    delete_window.configure(bg="#FFE4C4")

    # Label for the window
    delete_label = tk.Label(
        delete_window,
        text="Delete a Guest",
        font=("Times", 16, "bold"),
        bg="#FFE4C4",
        fg="#4B4B4B",
    )
    delete_label.pack(pady=20)

    id_label = tk.Label(
        delete_window,
        text="Enter Guest ID:",
        font=("Times", 12),
        bg="#FFE4C4",
        fg="#4B4B4B",
    )
    id_label.pack(anchor="w", padx=40, pady=5)

    id_entry = tk.Entry(delete_window, font=("Times", 12), width=30)
    id_entry.pack(padx=40, pady=10)

    def delete_guest():
        guest_id = id_entry.get()
        if not guest_id:
            messagebox.showerror("Error", "Guest ID cannot be empty!")
            return

        res = system.delete_guest(guest_id)
        if res:
            messagebox.showinfo(
                "Success", f"Guest with ID {guest_id} has been deleted successfully!")
            delete_window.destroy()
        else:
            messagebox.showerror(
                "Failure", f"Guest with ID {guest_id} Not Found!")
            delete_window.destroy()

    delete_button = tk.Button(
        delete_window,
        text="Delete",
        font=("Times", 12, "bold"),
        bg="#008CBA",
        fg="white",
        width=15,
        command=delete_guest,
    )
    delete_button.pack(pady=20)


def open_purchase_ticket_window():
    ticket_window = tk.Toplevel(root)
    ticket_window.title("Purchase Ticket")
    ticket_window.geometry("570x400")
    ticket_window.configure(bg="#FFE4C4")

    ticket_types = [
        "Single Day Pass",
        "Two Day Pass",
        "Annual Membership",
        "Child Ticket",
        "Group Ticket",
        "VIP Experience Pass",
    ]
    ticket_prices = {
        "Single Day Pass": 275,
        "Two Day Pass": 480,
        "Annual Membership": 1840,
        "Child Ticket": 185,
        "Group Ticket": 220,
        "VIP Experience Pass": 550,
    }
    selected_tickets = []
    total_price = tk.IntVar(value=0)

    order_id_label = tk.Label(
        ticket_window, text="Order ID:", font=("Times", 12), bg="#FFE4C4", fg="#4B4B4B"
    )
    order_id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    order_id_entry = tk.Entry(ticket_window, font=("Times", 12), width=20)
    order_id_entry.grid(row=0, column=1, padx=10, pady=10)

    registered_guests = system.get_registered_guests()
    guest_names = [guest.get_name() for guest in registered_guests]

    if len(guest_names) == 0:
        guest_names.append(["No Guests Available"])

    guest_label = tk.Label(
        ticket_window, text="Select Guest:", font=("Times", 12), bg="#FFE4C4", fg="#4B4B4B"
    )
    guest_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    guest_var = tk.StringVar(
        value=guest_names[0] if guest_names else "No Guests Available")
    guest_dropdown = tk.OptionMenu(ticket_window, guest_var, *guest_names)
    guest_dropdown.grid(row=1, column=1, padx=10, pady=10)

    ticket_label = tk.Label(
        ticket_window, text="Select Ticket Type:", font=("Times", 12), bg="#FFE4C4", fg="#4B4B4B"
    )
    ticket_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    ticket_var = tk.StringVar(value=ticket_types[0])  # Default value
    ticket_dropdown = tk.OptionMenu(ticket_window, ticket_var, *ticket_types)
    ticket_dropdown.grid(row=2, column=1, padx=10, pady=10)

    visit_date_label = tk.Label(
        ticket_window, text="Visit Date:", font=("Times", 12), bg="#FFE4C4", fg="#4B4B4B"
    )
    visit_date_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    visit_date_entry = tk.Entry(ticket_window, font=("Times", 12), width=20)
    visit_date_entry.grid(row=3, column=1, padx=10, pady=10)

    payment_method_label = tk.Label(
        ticket_window, text="Payment Method:", font=("Times", 12), bg="#FFE4C4", fg="#4B4B4B"
    )
    payment_method_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    payment_method_var = tk.StringVar(value="Credit Card")  # Default value
    payment_method_dropdown = tk.OptionMenu(
        ticket_window, payment_method_var, "Credit Card", "Digital Wallet", "Cash")
    payment_method_dropdown.grid(row=4, column=1, padx=10, pady=10)

    summary_label = tk.Label(
        ticket_window, text="Order Summary:", font=("Times", 12), bg="#FFE4C4", fg="#4B4B4B"
    )
    summary_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    summary_text = tk.Text(ticket_window, font=(
        "Times", 10), width=25, height=15, state="disabled")
    summary_text.grid(row=1, column=2, rowspan=4, padx=10, pady=10)

    tickets = []

    def add_ticket():
        global ticket_auto_id

        ticket = ticket_var.get()
        price = ticket_prices[ticket]
        selected_tickets.append((ticket, price))
        total_price.set(total_price.get() + price)

        summary_text.configure(state="normal")
        summary_text.delete(1.0, tk.END)
        for ticket, price in selected_tickets:
            summary_text.insert(tk.END, f"{ticket} - DHS{price}\n")
        summary_text.insert(tk.END, f"\nTotal Price: DHS{total_price.get()}")
        summary_text.configure(state="disabled")

        ticket_auto_id += 1

        # Use Ticket and TicketType for ticket creation
        ticket_type = TicketType[ticket.replace(" ", "_").upper()]
        ticket_obj = Ticket(ticket_auto_id, price, visit_date_entry.get().strip(), ticket_type)

        tickets.append(ticket_obj)

    add_ticket_button = tk.Button(
        ticket_window,
        text="Add Ticket",
        font=("Times", 12),
        bg="#008CBA",  # Green
        fg="white",
        command=add_ticket,
    )
    add_ticket_button.grid(row=5, column=0, columnspan=2, pady=10)

    total_order_amount = 0
    for i in tickets:
        total_order_amount += i.get_price()

    def confirm_order():
        order_id = order_id_entry.get()

        if not order_id or not tickets:
            messagebox.showerror("Error", "Please provide all required details and add at least one ticket.")
            return

        # Calculate the total price correctly
        total_order_amount = sum(ticket.get_price() for ticket in tickets)

        # Create the purchase order
        order = PurchaseOrder(order_id, tickets, total_order_amount, order_date=datetime.datetime.today())

        # Fetch the selected guest and add the order
        guest = system.fetch_guest_by_name(guest_var.get())
        if guest:
            guest.add_purchase_order(order_id, tickets, total_order_amount)

            # Update total sales in the system
            system.increase_total_sales(total_order_amount)

            messagebox.showinfo("Order Confirmed", "Your order has been successfully placed!")
        else:
            messagebox.showerror("Error", "Guest not found.")

        # Close the ticket window
        ticket_window.destroy()

    confirm_button = tk.Button(
        ticket_window,
        text="Confirm Order",
        font=("Times", 12, "bold"),
        bg="#008CBA",  # Blue
        fg="white",
        command=confirm_order,
    )
    confirm_button.grid(row=5, column=2, columnspan=2, pady=0)


def open_view_events_window():
    events_window = tk.Toplevel(root)
    events_window.title("View Events")
    events_window.geometry("400x400")
    events_window.configure(bg="#FFE4C4")

    # Add a heading label
    heading_label = tk.Label(
        events_window,
        text="Event List",
        font=("Times", 16, "bold"),
        bg="#FFE4C4",
        fg="#4B4B4B",
    )
    heading_label.pack(pady=10)

    # Get the list of events from the system
    events = system.get_events()

    # If no events are available
    if not events:
        no_events_label = tk.Label(
            events_window,
            text="No events available.",
            font=("Times", 12),
            bg="#FFE4C4",
            fg="#4B4B4B",
        )
        no_events_label.pack(pady=20)
        return

    # Create a frame to hold the list of events
    events_frame = tk.Frame(events_window, bg="#FFE4C4")
    events_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Add a scrollbar
    scrollbar = tk.Scrollbar(events_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    # Create a listbox to display events
    events_listbox = tk.Listbox(
        events_frame,
        font=("Times", 12),
        bg="#FFFFFF",
        fg="#000000",
        yscrollcommand=scrollbar.set,
        width=50,
        height=15,
    )
    events_listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=events_listbox.yview)

    # Populate the listbox with events
    for event in events:
        event_name = event.get_name()
        start_date = event.get_start_date()
        end_date = event.get_end_date()
        events_listbox.insert(
            tk.END, f"{event_name} - {start_date} to {end_date}")

    # Close button
    close_button = tk.Button(
        events_window,
        text="Close",
        font=("Times", 12, "bold"),
        bg="#008CBA",  # Red button
        fg="white",
        command=events_window.destroy,
    )
    close_button.pack(pady=10)

def admin_dashboard_window():
    services_window = tk.Toplevel(root)
    services_window.title("Admin Dashboard")
    services_window.geometry("400x400")
    services_window.configure(bg="#FFE4C4")

    # Variables
    ticket_types = [
        "Single Day Pass",
        "Two Day Pass",
        "Annual Membership",
        "Child Ticket",
        "Group Ticket",
        "VIP Experience Pass",
    ]

    # Fetch today's total sales
    total_sales = system.get_total_sales()

    # Display total sales for today
    sales_label_var = tk.StringVar(value=f"Total Ticket Sales Today: DHS{total_sales}")

    sales_label = tk.Label(
        services_window,
        textvariable=sales_label_var,
        font=("Times", 14, "bold"),
        bg="#FFE4C4",
        fg="#4B4B4B",
    )
    sales_label.pack(pady=20)

    # Dropdown to select ticket type
    ticket_label = tk.Label(
        services_window,
        text="Select Ticket Type:",
        font=("Times", 12),
        bg="#FFE4C4",
        fg="#4B4B4B",
    )
    ticket_label.pack(pady=10)

    ticket_var = tk.StringVar(value=ticket_types[0])  # Default value
    ticket_dropdown = tk.OptionMenu(services_window, ticket_var, *ticket_types)
    ticket_dropdown.pack(pady=10)

    # Text field for modifying ticket discount
    discount_label = tk.Label(
        services_window,
        text="Modify Discount Criteria:",
        font=("Times", 12),
        bg="#FFE4C4",
        fg="#4B4B4B",
    )
    discount_label.pack(pady=10)

    discount_entry = tk.Entry(services_window, font=("Times", 12), width=25)
    discount_entry.pack(pady=10)

    # Function to handle discount update and show pop-up
    def update_discount():
        ticket_type = ticket_var.get()
        new_discount = discount_entry.get()

        if not new_discount:
            messagebox.showerror("Error", "Please enter a new discount value!")
            return

        update_ticket_discount(ticket_type, new_discount)
        messagebox.showinfo("Success", f"Discount updated for {ticket_type} to '{new_discount}'.")

    # Button to update discount
    update_button = tk.Button(
        services_window,
        text="Update Discount",
        font=("Times", 12),
        bg="#008CBA",
        fg="white",
        width=20,
        command=update_discount,
    )
    update_button.pack(pady=20)

    # Button to refresh sales
    def refresh_sales():
        updated_sales = system.get_total_sales()
        sales_label_var.set(f"Total Ticket Sales Today: DHS{updated_sales}")

    refresh_sales_button = tk.Button(
        services_window,
        text="Refresh Sales",
        font=("Times", 12),
        bg="#008CBA",
        fg="white",
        width=20,
        command=refresh_sales,
    )
    refresh_sales_button.pack(pady=20)

# Placeholder for the update logic, to be implemented separately


def update_ticket_discount(ticket_type, new_discount_criteria):

    global single_day_pass_discount, two_day_pass_discount
    global annual_membership_discount, child_ticket_discount
    global group_ticket_discount, vip_experience_discount

    if ticket_type == "Single Day Pass":
        single_day_pass_discount = new_discount_criteria
    elif ticket_type == "Two Day Pass":
        two_day_pass_discount = new_discount_criteria
    elif ticket_type == "Annual Membership":
        annual_membership_discount = new_discount_criteria
    elif ticket_type == "Child Ticket":
        child_ticket_discount = new_discount_criteria
    elif ticket_type == "Group Ticket":
        group_ticket_discount = new_discount_criteria
    elif ticket_type == "VIP Experience Pass":
        vip_experience_discount = new_discount_criteria

    print(f"Updating {ticket_type} with new discount: {new_discount_criteria}")
    # Logic to update the ticket's discount goes here


def open_view_purchase_history_window():
    history_window = tk.Toplevel(root)
    history_window.title("View Purchase History")
    history_window.geometry("500x500")
    history_window.configure(bg="#FFE4C4")

    # Fetch registered guests from the system
    registered_guests = system.get_registered_guests()
    guest_names = [guest.get_name()
                   for guest in registered_guests]  # Extract guest names

    # Fallback if no guests are registered
    if not guest_names:
        guest_names.append("No Guests Available")

    # Guest selection dropdown
    guest_label = tk.Label(
        history_window, text="Select Guest:", font=("Times", 12), bg="#FFE4C4", fg="#4B4B4B"
    )
    guest_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Default value for guest dropdown
    guest_var = tk.StringVar(value=guest_names[0])
    guest_dropdown = tk.OptionMenu(history_window, guest_var, *guest_names)
    guest_dropdown.grid(row=0, column=1, padx=10, pady=10)

    # Text box to display purchase history
    history_label = tk.Label(
        history_window, text="Purchase History:", font=("Times", 12, "bold"), bg="#FFE4C4", fg="#4B4B4B"
    )
    history_label.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

    history_text = tk.Text(history_window, font=(
        "Times", 8), width=50, height=15, wrap="word")
    history_text.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    # Function to fetch and display purchase history
    def show_purchase_history():
        selected_guest_name = guest_var.get()

        # Clear previous history
        history_text.delete("1.0", tk.END)

        # Validate if the selected guest is valid
        if selected_guest_name == "No Guests Available":
            history_text.insert(tk.END, "No guests registered.")
            return

        # Fetch and display purchase history
        purchase_history = system.fetch_guest_purchase_history(selected_guest_name)

        # Display the result (handles both cases: no guest found or no purchase history)
        history_text.insert(tk.END, purchase_history)

        # Fetch and display purchase history
        purchase_history = system.fetch_guest_purchase_history(
            selected_guest_name)

        if not purchase_history:
            history_text.insert(
                tk.END, "No purchase history available for this guest.")
        else:
            history_text.insert(
                tk.END,
                purchase_history)

    # Button to fetch and show purchase history
    fetch_button = tk.Button(
        history_window,
        text="Show History",
        font=("Times", 12, "bold"),
        bg="#008CBA",
        fg="white",
        command=show_purchase_history,
    )
    fetch_button.grid(row=2, column=1, pady=10, sticky="e")

    # Close button
    close_button = tk.Button(
        history_window,
        text="Close",
        font=("Times", 12, "bold"),
        bg="#008CBA",
        fg="white",
        command=history_window.destroy,
    )
    close_button.grid(row=2, column=2, pady=10, sticky="w")


def open_view_tickets_window():
    events_window = tk.Toplevel(root)
    events_window.title("View Tickets")
    events_window.geometry("400x400")
    events_window.configure(bg="#FFE4C4")

    # Add a heading label
    heading_label = tk.Label(
        events_window,
        text="List of Tickets",
        font=("Times", 16, "bold"),
        bg="#FFE4C4",
        fg="#4B4B4B",
    )
    heading_label.pack(pady=10)

    # Get the list of events from the system
    tickets = system.get_tickets()

    # If no events are available
    if not tickets:
        no_events_label = tk.Label(
            events_window,
            text="No tickets available.",
            font=("Times", 12),
            bg="#FFE4C4",
            fg="#4B4B4B",
        )
        no_events_label.pack(pady=20)
        return

    # Create a frame to hold the list of events
    events_frame = tk.Frame(events_window, bg="#FFE4C4")
    events_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Add a scrollbar
    scrollbar = tk.Scrollbar(events_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    # Create a listbox to display events
    tickets_listbox = tk.Listbox(
        events_frame,
        font=("Times", 12),
        bg="#FFFFFF",
        fg="#000000",
        yscrollcommand=scrollbar.set,
        width=50,
        height=15,
    )
    tickets_listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=tickets_listbox.yview)

    # Populate the listbox with events
    for ticket in tickets:
        # Use the TicketType enum for matching ticket details
        ticket_type = ticket.get_ticket_type()  # This returns the Enum name
        ticket_price = ticket.get_price()
        ticket_discount = ticket.get_discount_available()
        ticket_description = ticket.get_description()

        # Insert ticket details in multiline format
        tickets_listbox.insert(tk.END, f"Name: {ticket_type.replace('_', ' ').title()}")
        tickets_listbox.insert(tk.END, f"Price: DHS{ticket_price:.2f}")
        tickets_listbox.insert(tk.END, f"Discount: {ticket_discount}")
        tickets_listbox.insert(tk.END, f"Description: {ticket_description}")
        # Add a blank line for separation
        tickets_listbox.insert(tk.END, "*******************")

    # Close button
    close_button = tk.Button(
        events_window,
        text="Close",
        font=("Times", 12, "bold"),
        bg="#008CBA",  # Red button
        fg="white",
        command=events_window.destroy,
    )
    close_button.pack(pady=10)


# Create the main window
root = tk.Tk()
root.title("Ticket Booking System")
window_width = 800
window_height = 450
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.configure(bg="#FFE4C4")

# Add a heading label
heading_label = tk.Label(
    root,
    text="Ticket Booking System",
    font=("Times", 20, "bold"),
    pady=20,
    bg="#FFE4C4",
    fg="#4B4B4B",
)
heading_label.pack()

# Add a right-side frame for actions
right_frame = tk.Frame(root, bg="#F8F8F8", width=200,
                       relief="solid", borderwidth=1, height=300)
right_frame.pack(side="right", fill="y", padx=20, pady=10)

# Add buttons inside the right frame
register_button = tk.Button(
    right_frame,
    text="Register Guest",
    font=("Times", 12),
    bg="#ADD8E6",
    fg="black",
    width=20,
    pady=5,
    command=open_registration_window,
)
register_button.pack(pady=10)

delete_button = tk.Button(
    right_frame,
    text="Delete Guest",
    font=("Times", 12),
    bg="#ADD8E6",
    fg="black",
    width=20,
    pady=5,
    command=open_delete_guest_window,
)
delete_button.pack(pady=10)

# Add buttons on the left side
purchase_ticket_button = tk.Button(
    root,
    text="Purchase Ticket",
    font=("Times", 12),
    bg="#ADD8E6",
    fg="black",
    width=20,
    pady=5,
    command=open_purchase_ticket_window,
)
purchase_ticket_button.pack(anchor="w", padx=40, pady=10)

view_events_button = tk.Button(
    root,
    text="View Events",
    font=("Times", 12),
    bg="#ADD8E6",
    fg="black",
    width=20,
    pady=5,
    command=open_view_events_window,
)
view_events_button.pack(anchor="w", padx=40, pady=10)

view_tickets_button = tk.Button(
    root,
    text="View Tickets",
    font=("Times", 12),
    bg="#ADD8E6",
    fg="black",
    width=20,
    pady=5,
    command=open_view_tickets_window,
)
view_tickets_button.pack(anchor="w", padx=40, pady=10)

view_history_button = tk.Button(
    root,
    text="View Guest Purchase History",
    font=("Times", 12),
    bg="#ADD8E6",
    fg="black",
    width=30,
    pady=5,
    command=open_view_purchase_history_window,
)
view_history_button.pack(anchor="w", padx=40, pady=10)


admin_button = tk.Button(
    root,
    text="Admin Dashboard",
    font=("Times", 12),
    bg="#ADD8E6",
    fg="black",
    width=20,
    pady=5,
    command=admin_dashboard_window,)
admin_button.pack(anchor="w", padx=40, pady=10)

# Start the tkinter main loop
root.mainloop()
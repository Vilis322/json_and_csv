from task1 import task1
from task2 import task2
from task3 import task3
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - [%(name)s] - %(message)s",
                    filename="logfile.log"
                    )


def main():
    choice = ""
    while choice != "4":
        print("\n=== MAIN MENU ===")
        print("Type '1' to run Task 1 (Students JSON)")
        print("Type '2' to run Task 2 (Sales CSV)")
        print("Type '3' to run Task 3 (Employees + Performance)")
        print("Type '4' to quit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            task1()
        elif choice == "2":
            task2()
        elif choice == "3":
            task3()
        elif choice == "4":
            print("Thank you for using this program!")
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

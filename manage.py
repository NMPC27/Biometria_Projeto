import os


def list_users():
    #list directories on /db
    print("Users:")
    for user in os.listdir("./db"):
        #if directory
        if os.path.isdir("./db/"+user):
            #see if fingerid.txt exists
            idx = None
            image = False
            if os.path.exists("./db/"+user+"/fingerid.txt"):
                #read fingerid.txt
                with open("./db/"+user+"/fingerid.txt", "r") as f:
                    idx = int(f.read())
            
            #see if image exists
            if os.path.exists("./db/"+user+"/user.png"):
                image = True
                
            print(user, idx, image)
            
def list_fingerprints():
    from fingerprint import finger
    finger.read_templates()
    print
    

def clear_fingerprint(idx):
    fingerprint.finger.delete_model(idx)        
            
        


def menu():
    print("1. List users")
    print("2. Delete user")
    print("3. Clear fingerprint sensor")
    print("4. Clear specific fingerprint")

if __name__ == "__main__":
    menu()
    choice = input("Enter choice: ")
    print("\n")
    if choice == "1":
        list_users()
    elif choice == "2":
        user = input("Enter user: ")
        if os.path.isdir("./db/"+user):
            if os.path.exists("./db/"+user+"/fingerid.txt"):
                import fingerprint
                with open("./db/"+user+"/fingerid.txt", "r") as f:
                    idx = int(f.read())
                clear_fingerprint(idx)

            #remove dir and all files inside
            for file in os.listdir("./db/"+user):
                os.remove("./db/"+user+"/"+file)
            os.rmdir("./db/"+user)
            print("Deleted user")
        else:
            print("User does not exist")
    elif choice == "3":
        import fingerprint
        fingerprint.clear_sensor()
    elif choice == "4":
        import fingerprint
        fingerprint.finger.read_templates()
        print(fingerprint.finger.templates)
        idx = int(input("Enter fingerprint id: "))
        clear_fingerprint(idx)
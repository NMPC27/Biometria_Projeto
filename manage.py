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
    
    
def gamma_correction():
    #show camera feed
    import cv2
    import numpy as np
    cap = cv2.VideoCapture(2)
    gamma = 1.0
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        
               #adjust  gamma
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
            for i in np.arange(0, 256)]).astype("uint8")
        frame = cv2.LUT(frame, table)
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        elif key == ord('d'):
            gamma += 0.1
            print(gamma)
        elif key == ord('a'):
            gamma -= 0.1
            print(gamma)
        
    cap.release()
    cv2.destroyAllWindows()
    
        


def menu():
    print("1. List users")
    print("2. Delete user")
    print("3. Clear fingerprint sensor")
    print("4. Clear specific fingerprint")
    print("5. adjust camera gamma")

if __name__ == "__main__":
    menu()
    choice = input("Enter choice: ")
    print("\n")
    if choice == "1":
        list_users()
    elif choice == "2":
        list_users()
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
        
    elif choice == "5":
        gamma_correction()
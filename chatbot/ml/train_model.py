import joblib

# for splitting the data in train(80 %) and test(20 %) split karny ky liyee :

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# lets take an dataset of about 4 key value pairs and then also is used to train the model :

training_data = {

    "add_user": [
        "can you add the user john.smith@xyz.com with phone number +92332",
        "add a new user samantha@abc.com with phone 03211234567",
        "please add user ali@company.com with phone number 03451234567",
        "create a new user with email test@site.com and phone 03009876543",
        "add user hamza@xyz.com with phone number 03219998888",
        "i want to add a user named sara with email sara@abc.com",
        "please create a new user john@example.com",
        "add a new account for david@gmail.com",
        "can you create a user with email michael@company.com",
        "i need to add a new user alice@xyz.com",
        "please register a new user with email robert@test.com",
        "create user emily@abc.com with phone 03123456789",
        "add james@gmail.com to the system",
        "please add another user named william",
        "create a new account for sophia@company.com",
        "i want to register user oliver@example.com",
        "add user charlotte@test.com with phone 03001234567",
        "can you create an account for daniel@xyz.com",
        "please add user grace@abc.com",
        "register a new user ethan@company.com",
        "add Rehman with email reh@gmail.com",
        "please add the user Rehman with email reh@gmail.com",
        "create an account for Rehman using email reh@gmail.com",
        "add user Rehman with email \"reh@gmail.com\"",
        "can you add Rehman to the system with email reh@gmail.com"
        "add the user Rehman with email reh@gmail.com and phone 03001234567",
        "can you add Rehman to the system with email reh@gmail.com",
        "please create a user named Ahmed with email ahmed@gmail.com",
        "register Fatima with email fatima@example.com and phone 03112223344",
        "I need to create an account for Hassan with email hassan@company.com",
        "add a new user Bilal and use bilal@test.com as his email",
        "please add Maria with phone number 03225556677",
        "create a user account for Usman with email usman@xyz.com",
        "can you register Ayesha using ayesha@gmail.com",
        "add the following user: name Zain, email zain@example.com",
        "I want to create a new account for Hina with phone 03334445566",
        "please register the user Ahmed Khan with email ahmedkhan@company.com",
        "add this user to the system: Sara, sara@test.com, 03001112233",
        "create an account for Hamza and set his email to hamza@gmail.com",
        "can you add a new user named Rehman with email \"reh@gmail.com\""
    ],


    "remove_user": [
        "can you remove the user john.smith@xyz.com",
        "delete user samantha@abc.com",
        "please remove ali@company.com from the system",
        "remove this user test@site.com",
        "delete the account of hamza@xyz.com",
        "get rid of user sara@abc.com",
        "please delete john@example.com",
        "remove david@gmail.com from the system",
        "can you delete the user michael@company.com",
        "i want to remove alice@xyz.com",
        "delete robert@test.com",
        "please remove emily@abc.com",
        "remove james@gmail.com from the database",
        "delete the account belonging to william@example.com",
        "can you get rid of sophia@company.com",
        "please delete user oliver@example.com",
        "remove charlotte@test.com",
        "remove the user fatima with email fatima@gmail.com and phone 087464"
        "i want to delete daniel@xyz.com",
        "please remove grace@abc.com",
        "delete ethan@company.com from the system",
        "remove Rehman with email reh@gmail.com",
        "remove the user Rehman with email reh@gmail.com",
        "delete Rehman using email reh@gmail.com",
        "please delete Rehman with email \"reh@gmail.com\"",
        "get rid of Rehman from the system using email reh@gmail.com"
        "remove Rehman from the system",
        "delete the user Rehman",
        "please remove Rehman with email reh@gmail.com",
        "can you delete Rehman using his email reh@gmail.com",
        "get rid of the account for Rehman",
        "remove the user with email reh@gmail.com",
        "delete the account associated with reh@gmail.com",
        "please erase the user Ahmed from the system",
        "I want to delete the account of Fatima",
        "can you remove Bilal from the database",
        "please delete user Hassan with email hassan@company.com",
        "remove the account belonging to Ayesha",
        "delete Maria using email maria@example.com",
        "I need to remove Zain from the user list",
        "please delete the user with email \"reh@gmail.com\""
    ],


    "update_user": [
        "can you update samanthas city to Cordoba",
        "update johns phone number to 03211234567",
        "change alis email to newali@company.com",
        "update the city of hamza to Lahore",
        "please change saras phone to 03009998888",
        "update user samantha city to Karachi",
        "change johns email to johnnew@example.com",
        "update david phone number to 03112223344",
        "please change michaels city to Islamabad",
        "update alice email to alice_new@xyz.com",
        "change roberts phone number to 03456789012",
        "please update emilys city to Lahore",
        "change james email to james_new@gmail.com",
        "update williams phone number to 03001112223",
        "please change sophias city to Karachi",
        "update olivers email address to oliver_new@example.com",
        "change charlottes phone to 03224445566",
        "please update daniels city to Sialkot",
        "change graces email to grace_new@abc.com",
        "update ethans phone number to 03335557788",
        "change Rehmans city to Lahore",
        "update Rehman phone number to 03001234567",
        "change Rehmans email to newrehman@gmail.com",
        "please update Rehman city from Sialkot to Lahore",
        "update the user Rehman phone number to +923001234567"
        "change Rehmans city to Lahore",
        "update Rehman phone number to 03001234567",
        "change Rehmans email to rehman_new@gmail.com",
        "please update Ahmeds city to Islamabad",
        "change Fatimas phone to 03112223344",
        "update Hassans email address to hassan_new@company.com",
        "modify Bilals city to Karachi",
        "please change Ayeshas phone number to 03225556677",
        "update Zains email to zain_new@example.com",
        "I want to change Hinas city to Sialkot",
        "please update Usmans phone number to 03334445566",
        "change Marias email address to maria_new@gmail.com",
        "modify Rehmans phone number to +923001234567",
        "update the city of Ahmed from Lahore to Islamabad",
        "change the user Rehmans email to \"rehman_new@gmail.com\""
    ],


    "unknown": [
        "what is the weather today",
        "hello how are you",
        "tell me a joke",
        "what time is it",
        "thank you very much",
        "what is the capital of Pakistan",
        "how are you doing",
        "tell me something interesting",
        "what is the temperature today",
        "who is the president of Pakistan",
        "can you tell me a story",
        "good morning",
        "good evening",
        "what day is today",
        "help me with my homework",
        "tell me a funny joke",
        "what is the meaning of artificial intelligence",
        "how old are you",
        "what is Python",
        "who created the internet",
        "what is the best programming language",
        "tell me about machine learning",
        "how does artificial intelligence work",
        "what is the capital city of France",
        "can you explain Python to me"
        "what is the weather like today",
        "tell me today's temperature",
        "what is the capital of Germany",
        "who invented the computer",
        "explain what machine learning is",
        "what can Python be used for",
        "tell me an interesting fact",
        "can you tell me a joke",
        "what time is it",
        "what day is it today",
        "good afternoon",
        "how are you today",
        "what is the meaning of cloud computing",
        "can you help me understand artificial intelligence",
        "tell me something about databases"
    ]
}

phrases = []

labels = []

for intent, examples in training_data.items():
    for examp in examples:
        phrases.append(examp)
        labels.append(intent)

print(f"Total Examples : {len(phrases)}")

print(f"intents : {labels}")

# Now train and test :

X_train, X_test, y_train, y_test = train_test_split(
    phrases, labels, test_size=0.20, random_state=42
)

# IFiffVectorizer used to check the imporatnce rate of every word in the column an also in all phrases :

vectorizer = TfidfVectorizer(ngram_range=(1, 2))

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Now I train the model :

model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Testing :

y_pred = model.predict(X_test_vec)

# printing performance score :
print(f"Accuracy : {accuracy_score(y_test, y_pred)}")

# printing confidence score :
print(classification_report(y_test, y_pred))

# Now I vectorixe the modal based on whole data :

final_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X_all_vec = final_vectorizer.fit_transform(phrases)

# Now lets train the model based on whole data as input :
final_model = MultinomialNB()
final_model.fit(X_all_vec, labels)


joblib.dump(final_model, "chatbot/ml/model.pkl")
joblib.dump(final_vectorizer, "chatbot/ml/vectorizer.pkl")

print("Model and vectorizer save Succesfully!")
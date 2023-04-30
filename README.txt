
Inspiration

While being shown a tour of George Mason, our home university, we were introduced to a program called the "Patriot Pantry". The idea behind this is a program to help address food insecurities for George Mason students as 1 in 4 college students face some kind of food insecurity, they aimed to solve this problem which many students face by encouraging plant growth to provide low cost options for students. After further thought on this we were reminded of a small gym check in app called GymRats which encourages friendly competition between people regarding gym attendance consistency. We noticed how this had a positive impact on us and our friends in encouraging more healthy behavior through competition. From these two things we began to come up with an idea for PAPA, a system to help encourage a more environmentally conscious and healthy world.
What it does

PAPA, or the Perfect Application for Plant Assistance, is both a web application and IoT device which helps to encourage people to grow plants of various kinds through demystifying the botany process while encouraging friendly competition amongst groups of people to motivate plant growth to improve issues of air pollution and food insecurity. PAPA can be implemented in an already established garden or can be used for those curious about trying something new. PAPA allows for users to either use purely the web application allowing for a helpful amount of features, as well as providing access to our custom made IoT device which provides access to a wide arrangement of various data relevant to plant growth. Once ready to use PAPA all you have to do is upload an image of your plant to our web application. Once there our custom trained deep learning model will classify the type of plant that it is. From there it uses our PAPA AI model to provide clear, accurate, and helpful information which is given back to the user. Information you will receive will be relevant to your area and localized weather. If you chose to use our seed device you will also gain access to temperature, atmospheric pressure, humidity, ambient light information, volatile organic compounds data, and CO2 levels which can be specific to the room the seed system is in. All of these can be given back to the user alerting them if there are any issues or important recommendations which could be made. Using these systems it can even be possible to do early detection of issues related to pest infestation as those can be related to any of the previously listed data being off from what it should be. Along with this PAPA also encourages learning through a text system with our PAPA AI which can provide helpful tips and information based on your specific plant and the environment around it. Along with this PAPA also has a gamified system to encourage users to follow helpful advice and grow more plants. With a point system which rewards users on leader-boards for growing more plants and growing plants well as the health of the plant can be checked through gathered data from the seed system. All of this comes together to help encourage people to grow more plants helping to solve worldwide issues of food insecurities and air pollution.
How we built it

The Deep Learning model used for image identification and classification was made using tensorflow keras models. It is a custom trained CNN model which can identify various plants as their scientific name and then feed that information to PAPA AI. PAPA AI is built using gpt-3.5 and returns information about a given plant based on the provided scientific name, weather data, and seed data. Weather information is gathered through pulling metadata off of uploaded images to get the location of where the photo was taken from. After that it uses openweather api to get current weather information like temperature, general description, and humidity which it also sends to PAPA AI. We used an ESP32 micro controller with various sensors to create our seed device which communicates crucial data to our website and provides the user with data regarding specifics to the rooms environment. For the webpage we utilized tornado for web development and fast-api to create different apis for our product. We securely stored user data in a secure database which had encryption with user based object-oriented programming.
Challenges we ran into

For our AI we ran into the challenge of overfitting our data which occurs when there is an uneven amount of data for one identification or if the same data is shown to the model during training too many times. This can lead to the model always guessing that a prediction is whichever identity it saw the most during training was, causing the accuracy of the model in training to be higher however in actual implementation this dramatically decreases. We prevented this issue by keeping our epoch count to 10, the standard of deep learning training epochs. We also ensured out dataset was shuffled during training to ensure there was no favoritism in predictions from the model.
Accomplishments that we're proud of

We're extremely proud of our deep learning model's 98.9% accuracy in plant classification and identification through the trained dataset. We are also proud of the look of our website as well as being able to effectively gather vast amounts of information and display it to the user in a friendly way.
What we learned

We learned various new things working on this project. Including usage and implementation of tensorflow to create a deep learning CNN for image classification. We also learned many things about web development and secure data storage practices.
What's next for PAPA

Our future goals for PAPA are to gather more data for our custom Deep Learning model and to expand our user point system as well as improve our overall GUI
Built With

    ai
    cnn
    deep-learning
    openai
    openweather
    python
    tensorflow

Try it out

from wordcloud import WordCloud
import matplotlib.pyplot as plt


def a():
    """histogram of the letters"""
    with open('file.txt', 'r') as f:
        text = f.read()
        text = text.lower()
        # create a dictionary with the letters
        letters = {}
        for letter in text:
            if letter.isalpha():
                if letter in letters:
                    letters[letter] += 1
                else:
                    letters[letter] = 1
        # print the dictionary
        for key, value in sorted(letters.items()):
            print(key, value)
            
def c(words):
        """word cloud"""

        wordcloud = WordCloud()
        wordcloud.generate_from_frequencies(frequencies=words)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()
        
def b():
    """histogram of the words"""
    with open("file.txt", 'r') as f:
        text = f.read()
        text = text.lower()
        #remove punctuation
        for char in '.,;:!?':
            text = text.replace(char, '')
        # create a dictionary with the words
        words = {}
        for word in text.split():
            if word in words:
                words[word] += 1
            else:
                words[word] = 1
        # print the dictionary
        for key, value in sorted(words.items()):
            print(key, value)
        
    choice = input('Do you want a word cloud? (y/n): ')
    if choice == 'y':
        c(words)
    else:
        pass

    
def main():
    #choose a or b
    choice = input('Choose a (letters) or b (words): ')
    if choice == 'a':
        a()
    else:
        b()

        
if __name__ == '__main__':
    main()

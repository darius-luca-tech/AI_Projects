import os 
  
# Function to rename multiple files 
def main(): 
    i = 29
      
    for filename in os.listdir("toothbrush/"): 
        dst ="image" + str(i) + ".jpg"
        src ='toothbrush/'+ filename 
        dst ='toothbrush/'+ dst 
          
        # rename() function will 
        # rename all the files 
        os.rename(src, dst) 
        i += 1
  
# Driver Code 
if __name__ == '__main__': 
      
    # Calling main() function 
    main() 

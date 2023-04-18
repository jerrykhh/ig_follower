from ig.file import ImageFileSaveQueue, FetchImageFile
import time

if __name__ == "__main__":
    print("queue created")
    q = ImageFileSaveQueue.get_instance()
    q.start()

    q.put(FetchImageFile(id=None, url="https://instagram.fhkg1-1.fna.fbcdn.net/v/t51.2885-15/25022529_132960970732521_1326363167466455040_n.jpg?stp=dst-jpg_e35&_nc_ht=instagram.fhkg1-1.fna.fbcdn.net&_nc_cat=109&_nc_ohc=jNREJo0IS0MAX-tuI9V&edm=ACWDqb8BAAAA&ccb=7-5&ig_cache_key=MTY3NTA3ODQxMzcyNTg1MDY0OA%3D%3D.2-ccb7-5&oh=00_AfBgpH78N7ti5ijiFVP3aOStIePRdgoG9JJD13tCIN2Ytw&oe=64448615&_nc_sid=1527a3" \
                            ,output_path="./output/"))

    print("sleep 2")
    time.sleep(2)

    q.put(FetchImageFile(id=None, url="https://instagram.fhkg1-1.fna.fbcdn.net/v/t51.2885-15/25022529_132960970732521_1326363167466455040_n.jpg?stp=dst-jpg_e35&_nc_ht=instagram.fhkg1-1.fna.fbcdn.net&_nc_cat=109&_nc_ohc=jNREJo0IS0MAX-tuI9V&edm=ACWDqb8BAAAA&ccb=7-5&ig_cache_key=MTY3NTA3ODQxMzcyNTg1MDY0OA%3D%3D.2-ccb7-5&oh=00_AfBgpH78N7ti5ijiFVP3aOStIePRdgoG9JJD13tCIN2Ytw&oe=64448615&_nc_sid=1527a3" \
                            ,output_path="./output/"))


    q.put(FetchImageFile(id=None, url="https://instagram.fhkg1-1.fna.fbcdn.net/v/t51.2885-15/25022529_132960970732521_1326363167466455040_n.jpg?stp=dst-jpg_e35&_nc_ht=instagram.fhkg1-1.fna.fbcdn.net&_nc_cat=109&_nc_ohc=jNREJo0IS0MAX-tuI9V&edm=ACWDqb8BAAAA&ccb=7-5&ig_cache_key=MTY3NTA3ODQxMzcyNTg1MDY0OA%3D%3D.2-ccb7-5&oh=00_AfBgpH78N7ti5ijiFVP3aOStIePRdgoG9JJD13tCIN2Ytw&oe=64448615&_nc_sid=1527a3" \
                            ,output_path="./output/"))


    q.put(FetchImageFile(id=None, url="https://instagram.fhkg1-1.fna.fbcdn.net/v/t51.2885-15/25022529_132960970732521_1326363167466455040_n.jpg?stp=dst-jpg_e35&_nc_ht=instagram.fhkg1-1.fna.fbcdn.net&_nc_cat=109&_nc_ohc=jNREJo0IS0MAX-tuI9V&edm=ACWDqb8BAAAA&ccb=7-5&ig_cache_key=MTY3NTA3ODQxMzcyNTg1MDY0OA%3D%3D.2-ccb7-5&oh=00_AfBgpH78N7ti5ijiFVP3aOStIePRdgoG9JJD13tCIN2Ytw&oe=64448615&_nc_sid=1527a3" \
                            ,output_path="./output/"))

    print("sleep 3")
    time.sleep(3)


    q.put(FetchImageFile(id=None, url="https://instagram.fhkg1-1.fna.fbcdn.net/v/t51.2885-15/25022529_132960970732521_1326363167466455040_n.jpg?stp=dst-jpg_e35&_nc_ht=instagram.fhkg1-1.fna.fbcdn.net&_nc_cat=109&_nc_ohc=jNREJo0IS0MAX-tuI9V&edm=ACWDqb8BAAAA&ccb=7-5&ig_cache_key=MTY3NTA3ODQxMzcyNTg1MDY0OA%3D%3D.2-ccb7-5&oh=00_AfBgpH78N7ti5ijiFVP3aOStIePRdgoG9JJD13tCIN2Ytw&oe=64448615&_nc_sid=1527a3" \
                            ,output_path="./output/"))


    q.put(FetchImageFile(id=None, url="https://instagram.fhkg1-1.fna.fbcdn.net/v/t51.2885-15/25022529_132960970732521_1326363167466455040_n.jpg?stp=dst-jpg_e35&_nc_ht=instagram.fhkg1-1.fna.fbcdn.net&_nc_cat=109&_nc_ohc=jNREJo0IS0MAX-tuI9V&edm=ACWDqb8BAAAA&ccb=7-5&ig_cache_key=MTY3NTA3ODQxMzcyNTg1MDY0OA%3D%3D.2-ccb7-5&oh=00_AfBgpH78N7ti5ijiFVP3aOStIePRdgoG9JJD13tCIN2Ytw&oe=64448615&_nc_sid=1527a3" \
                            ,output_path="./output/"))


    q.put(FetchImageFile(id=None, url="https://instagram.fhkg1-1.fna.fbcdn.net/v/t51.2885-15/25022529_132960970732521_1326363167466455040_n.jpg?stp=dst-jpg_e35&_nc_ht=instagram.fhkg1-1.fna.fbcdn.net&_nc_cat=109&_nc_ohc=jNREJo0IS0MAX-tuI9V&edm=ACWDqb8BAAAA&ccb=7-5&ig_cache_key=MTY3NTA3ODQxMzcyNTg1MDY0OA%3D%3D.2-ccb7-5&oh=00_AfBgpH78N7ti5ijiFVP3aOStIePRdgoG9JJD13tCIN2Ytw&oe=64448615&_nc_sid=1527a3" \
                            ,output_path="./output/"))

    q.put(FetchImageFile(id=None, url="https://instagram.fhkg1-1.fna.fbcdn.net/v/t51.2885-15/25022529_132960970732521_1326363167466455040_n.jpg?stp=dst-jpg_e35&_nc_ht=instagram.fhkg1-1.fna.fbcdn.net&_nc_cat=109&_nc_ohc=jNREJo0IS0MAX-tuI9V&edm=ACWDqb8BAAAA&ccb=7-5&ig_cache_key=MTY3NTA3ODQxMzcyNTg1MDY0OA%3D%3D.2-ccb7-5&oh=00_AfBgpH78N7ti5ijiFVP3aOStIePRdgoG9JJD13tCIN2Ytw&oe=64448615&_nc_sid=1527a3" \
                            ,output_path="./output/"))

    print("sleep 1")
    time.sleep(1)

    q.put(FetchImageFile(id=None, url="https://instagram.fhkg1-1.fna.fbcdn.net/v/t51.2885-15/25022529_132960970732521_1326363167466455040_n.jpg?stp=dst-jpg_e35&_nc_ht=instagram.fhkg1-1.fna.fbcdn.net&_nc_cat=109&_nc_ohc=jNREJo0IS0MAX-tuI9V&edm=ACWDqb8BAAAA&ccb=7-5&ig_cache_key=MTY3NTA3ODQxMzcyNTg1MDY0OA%3D%3D.2-ccb7-5&oh=00_AfBgpH78N7ti5ijiFVP3aOStIePRdgoG9JJD13tCIN2Ytw&oe=64448615&_nc_sid=1527a3" \
                            ,output_path="./output/"))
    print("sleep 5")
    time.sleep(5)

    q.put(FetchImageFile(id=None, url="https://instagram.fhkg1-1.fna.fbcdn.net/v/t51.2885-15/25022529_132960970732521_1326363167466455040_n.jpg?stp=dst-jpg_e35&_nc_ht=instagram.fhkg1-1.fna.fbcdn.net&_nc_cat=109&_nc_ohc=jNREJo0IS0MAX-tuI9V&edm=ACWDqb8BAAAA&ccb=7-5&ig_cache_key=MTY3NTA3ODQxMzcyNTg1MDY0OA%3D%3D.2-ccb7-5&oh=00_AfBgpH78N7ti5ijiFVP3aOStIePRdgoG9JJD13tCIN2Ytw&oe=64448615&_nc_sid=1527a3" \
                            ,output_path="./output/"))

    q.put(None)
    print("end")
import praw
import time
import os

log_file_path = "comment_log.txt"
rejected_file_path = "comment_rejected.txt"

def initialize_reddit():
    return praw.Reddit(
        client_id=" ",
        client_secret=" ",
        user_agent=" ",
        username=" ",
        password=" "
    )

def log_comment(comment_id, status):
    file_path = log_file_path if status == 'accepted' else rejected_file_path
    with open(file_path, "a") as log_file:
        log_file.write(comment_id + "\n")

def is_comment_logged(comment_id):
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as log_file:
            if comment_id in log_file.read().splitlines():
                return 'accepted'
    if os.path.exists(rejected_file_path):
        with open(rejected_file_path, "r") as log_file:
            if comment_id in log_file.read().splitlines():
                return 'rejected'
    return False

def vote_comment(comment, vote_type):
    if vote_type == 'upvote':
        comment.upvote()
        print("Upvoted the comment.")
    elif vote_type == 'downvote':
        comment.downvote()
        print("Downvoted the comment.")
    else:
        print("Invalid vote type.")

def reply_to_user_comments(reddit, target_user):
    try:
        for comment in reddit.redditor(target_user).comments.new(limit=None):
            status = is_comment_logged(comment.id)
            if status:
                continue
            if comment.author != reddit.user.me():
                print(f"\nComment found by {target_user}: {comment.body}")
                print(f"URL: https://www.reddit.com{comment.permalink}")
                while True:
                    user_input = input("\n1: Onayla ve standart cevapla\n2: Özel cevapla\n3: Reddet\n4: Kullanıcıyı değiştir\n5: Çıkış\n6: Otomatik upvote\n7: Otomatik downvote\nSeçiminizi yapın: ")

                    if user_input == "1":
                        comment.reply(response_message)
                        log_comment(comment.id, 'accepted')
                        print(f"Replied with: {response_message}")
                        print(f"Comment link: https://www.reddit.com{comment.permalink}")
                        break
                    elif user_input == "2":
                        custom_response = input("Özel yanıtınızı girin: ")
                        comment.reply(custom_response)
                        log_comment(comment.id, 'accepted')
                        print(f"Replied with: {custom_response}")
                        print(f"Comment link: https://www.reddit.com{comment.permalink}")
                        break
                    elif user_input == "3":
                        log_comment(comment.id, 'rejected')
                        print("Yorum reddedildi, bir sonraki yoruma geçiliyor.")
                        break
                    elif user_input == "4":
                        new_user = input("Yeni kullanıcı adını girin: ").strip()
                        if new_user:
                            return new_user
                        break
                    elif user_input == "5":
                        print("Çıkılıyor...")
                        exit()
                    elif user_input == "6":
                        vote_comment(comment, 'upvote')
                        log_comment(comment.id, 'accepted')
                        print(f"Comment link: https://www.reddit.com{comment.permalink}")
                        break
                    elif user_input == "7":
                        vote_comment(comment, 'downvote')
                        log_comment(comment.id, 'rejected')
                        print(f"Comment link: https://www.reddit.com{comment.permalink}")
                        break
                    else:
                        print("Geçersiz giriş, lütfen 1, 2, 3, 4, 5, 6 veya 7 girin.")
                time.sleep(10)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    target_user = input("Başlangıç kullanıcı adını girin: ").strip()
    reddit = initialize_reddit()
    
    while True:
        print(f"Şu anda kullanıcı: {target_user}")
        new_user = reply_to_user_comments(reddit, target_user)
        if new_user:
            target_user = new_user
            reddit = initialize_reddit()
        print("10 saniye boyunca bekleniyor...")
        time.sleep(10)

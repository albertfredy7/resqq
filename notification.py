import streamlit as st
import requests

ONESIGNAL_REST_API_KEY = 'Y2E1MGE0ZWMtYzdiOC00NzJlLWE2NGMtNGIyYzdmOGYwYTQ4'
ONESIGNAL_APP_ID = '59c1df58-c1a6-4686-a0e5-50739e1d794c'

@st.cache
def send_notification(message):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {ONESIGNAL_REST_API_KEY}"
    }
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "included_segments": ["All"],
        "contents": {"en": message}
    }
    response = requests.post("https://onesignal.com/api/v1/notifications", headers=headers, json=payload)
    return response

def main():
    st.title("Notification Sender")
    message = st.text_input("Enter notification message")
    if st.button("Send Notification"):
        response = send_notification(message)
        if response.status_code == 200:
            st.success("Notification sent successfully!")
        else:
            st.error("Failed to send notification.")

if __name__ == "__main__":
    main()

from parse import parse_email
email1 = """Hi Lenin,

Thank you for applying to the Software Engineer role at Google.

We would like to invite you to an interview as the next step in the process.

Please select a time that works for you:
https://calendly.com/google-interview

Looking forward to speaking with you.

Best,
John Carter
Google Recruiting Team
"""

email2 = """Hello Lenin,

Your interview with Meta has been scheduled for April 3, 2026 at 11:00 AM.

Join the meeting here:
https://zoom.us/j/987654321

Best regards,
Sarah Johnson
Meta Recruiting
"""

email3 = """Hi Lenin,

Thank you for your interest in Microsoft.

We regret to inform you that we will not be moving forward with your application at this time.

We appreciate your time and effort.

Sincerely,
Microsoft Hiring Team
"""

email4 = """Hello Lenin,

Thank you for your application to Spotify.

After careful consideration, we have decided to move forward with other candidates.

We encourage you to apply again in the future.

Best,
Spotify Recruitment Team
"""

email5 = """Hi Lenin,

Congratulations!

We are pleased to extend an offer for the position of Frontend Developer at Amazon.

You can review your offer details here:
https://amazon.jobs/offer

Start date: May 15, 2026

Best regards,
Amazon HR Team
"""

emails = [email1, email2, email3, email4, email5]


def main():
    for email in emails:
        print("Email:")
        print(email)
        print("Extracted Information:")
        print(parse_email(email))
        print("-" * 50)
    
if __name__ == "__main__":
    main()
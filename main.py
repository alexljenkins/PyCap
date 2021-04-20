def define_env(env):
    @env.macro
    def course_summary(title, date, description=None, prev_know=None, skills=None, mentors=None, links=None):

        site = env.conf["site_url"].strip("/")

        rows = [
            f"| Created date | { date } |",
            f"| Previous knowledge | { prev_know if prev_know is not None else 'None required'} |",
            f"""| What you will learn | {''.join([f'<div class="what-you-will-learn">{skill}</div>' for skill in skills])} |"""
            if skills is not None
            else "",
            f"""| Mentor{ 's' if len(mentors) > 1 else ''} | {''.join([f'<a href="{site}/contributing/#mentor-{mentor}"><img style="border-radius:50%;width:50px;height:50px;margin-right:8px;" src="https://github.com/{ mentor }.png"></a>' for mentor in mentors])} |"""
            if mentors is not None
            else "",
            f"""| Learning resource{ 's' if len(links) > 1 else ''} | {''.join([f'<div>{link}</div>' for link in links])} |"""
            if links is not None
            else "",
        ]

        rows = "\n".join(row for row in rows if row)

        return f"""# {title}
| Key | Info |
|-----|-------|
{rows}

{'## Description' if description else ''}

{f'<div style="text-align: justify"> { description } </div>' if description else ''}
"""

    @env.macro
    def mentor_summary(mentor):

        site = env.conf["site_url"].strip("/")

        return f"""
        <div id="mentor-{ mentor['github'] }" style="display: flex;margin-bottom:30px;">
            <img style="border-radius:50%;width:80px;height:80px" src="https://github.com/{ mentor['github'] }.png">
            <div style="flex-grow:1;margin-left:20px;" >
                <a href="https://github.com/{ mentor['github'] }">
                    <div>
                    { mentor['name'] }
                    </div>
                </a>
                <div>
                    {mentor['description']}
                </div>
                <div style="margin-top:10px;">
                    Courses
                    <ul style="margin-top:5px;">
                        {''.join([f'<a href="{site}/{ course }/"><li>{ course }</li></a>' for course in mentor['courses']]) }
                    </ul>
                </div>
            </div>
        </div>
        """.strip()

    @env.macro
    def certified(student):

        site = env.conf["site_url"].strip("/")

        return f"""
        <div id="mentor-{ student['github'] }" style="display: flex;margin-bottom:30px;align-items: center;">
            <img style="border-radius:50%;width:80px;height:80px" src="https://github.com/{ student['github'] }.png">
            <div style="flex-grow:1;margin-left:20px;" >
                <a href="https://github.com/{ student['github'] }">
                    <div>
                    { student['name'] }
                    </div>
                </a>
                <div>
                    Certificate: <a href="{student['badgr']}">View my certificate on Badgr!</a>
                </div>
                <div>
                    Capstone: <a href="{student['capstone']}">View my capstone on Github!</a>
                </div>
            </div>
        </div>
        """.strip()

    @env.macro
    def news(info, end_date):

        site = env.conf["site_url"].strip("/")

        return f"""
        <div id="news" end_date="{end_date}" class="admonition info" style="display:none;">
            <p class="admonition-title">Info</p>
            {info}
        </div>
<script>
var news = document.getElementById('news')
if (new Date() < new Date(news.getAttribute('end_date'))) {{
    news.style.display = 'block'
}}
</script>
        """.strip()

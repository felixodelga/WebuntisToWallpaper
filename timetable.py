import webuntis
import datetime


def getTimetable(day=datetime.date.today()):

    s = webuntis.Session(
        server='neilo.webuntis.com',
        school='bg-brg-keimgasse',
        username='of261002',
        password='7mof0975!',
        useragent='Odis-WebUntis-Scraper'
    )

    s.login()

    lesson_starttimes = [
        datetime.datetime.combine(day, datetime.time(hour=8, minute=0)),
        datetime.datetime.combine(day, datetime.time(hour=8, minute=55)),
        datetime.datetime.combine(day, datetime.time(hour=10, minute=0)),
        datetime.datetime.combine(day, datetime.time(hour=10, minute=55)),
        datetime.datetime.combine(day, datetime.time(hour=11, minute=50)),
        datetime.datetime.combine(day, datetime.time(hour=12, minute=45)),
        datetime.datetime.combine(day, datetime.time(hour=14, minute=0)),
        datetime.datetime.combine(day, datetime.time(hour=14, minute=50)),
        datetime.datetime.combine(day, datetime.time(hour=15, minute=40)),
        datetime.datetime.combine(day, datetime.time(hour=16, minute=30))
    ]

    # get list of subjects and timetable for 1 day
    suj = s.subjects()
    klasse = s.klassen().filter(name='7m')[0]
    tt = s.timetable(klasse=klasse, start=day, end=day)
    s.logout()

    # sort lessons by starttime
    lessons_sorted = []

    for time in lesson_starttimes:
        lessons_sorted.append(tt.filter(start=time))

    # result array
    timetable = []

    for lessons in lessons_sorted:
        l = len(lessons)

        # free
        if (l == 0):
            timetable.append([])

        else:

            to_append = []
            for i in range(len(lessons)):

                code = lessons[i].code

                # normal
                if (code == None):
                    to_append.append(suj.filter(
                        id=lessons[i].subjects[0].id)[0].name)

                else:

                    if (code == "cancelled"):
                        to_append.append(
                            '--' +
                            suj.filter(id=lessons[i].subjects[0].id)[0].name
                        )

                    if (code == "irregular"):
                        try:
                            to_append.append(
                                '++' +
                                suj.filter(id=lessons[i].subjects[0].id)[
                                    0].name
                            )
                        except IndexError:
                            to_append.append("failed")

            timetable.append(to_append)

    return timetable


if __name__ == '__main__':
    print(getTimetable())

import hug

from xml.sax import make_parser, handler

from textnormalize import text_normalize_filter


@hug.get(output=hug.output_format.pretty_json)
@hug.cli()
def parse_courses(filename:hug.types.text):
    """Parse course data from supplied log file name"""
    handler = RunningHandler()
    parser = make_parser()
    filter_handler = text_normalize_filter(parser, handler)
    filter_handler.parse(filename)
    return handler.course_dict


def parse_equipment(filename:hug.types.text):
    """Parse equipment data from supplied log file name"""
    pass


def parse_events(filename:hug.types.text):
    pass


class RunningHandler(handler.ContentHandler):
    """Content handler to parse the runningahead.com XML output"""
    # Define constants to record state
    CAPTURE_KEY = 1
    CAPTURE_COURSE = 2
    CAPTURE_PROPERTY = 3

    def __init__(self):
        self.course_dict = {}
        self.event_dict = {}
        self.equipment_dict = {}
        self._item_to_create = None
        self._state = None
        return

    def startElement(self, name, attrs):
        if name == "CourseCollection":
            self._curr_course = {}
        if name == "Course":
            self._curr_course["id"] = attrs["id"]

        if name in ["Name", "DefaultDistance"]:
            self._item_to_create = name.lower()
            self._state = self.CAPTURE_PROPERTY
        return

    def endElement(self, name):
        if name == "Course":
            self.course_dict[self._curr_course["id"]] = self._curr_course
            self._curr_course = {}

        if name in ["Name", "DefaultDistance"]:
            self._state = None
        return

    def characters(self, content):
        if self._state == self.CAPTURE_PROPERTY:
            self._curr_course[self._item_to_create] = content
        return


if __name__ == "__main__":
    parse_courses.interface.cli()

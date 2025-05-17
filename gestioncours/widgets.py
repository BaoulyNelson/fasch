from django.forms import TextInput, Textarea, CheckboxInput, DateInput, FileInput, EmailInput, Select,NumberInput,PasswordInput,ClearableFileInput,URLInput



base_classes = "block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"

class TailwindNumberInput(NumberInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({
            'class': 'block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500'
        })
        super().__init__(*args, **kwargs)
        
        
class TailwindInput(TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {"class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"})
        super().__init__(*args, **kwargs)

class TailwindTextarea(Textarea):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {"class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"})
        super().__init__(*args, **kwargs)

class TailwindCheckbox(CheckboxInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {"class": "form-checkbox h-5 w-5 text-blue-600"})
        super().__init__(*args, **kwargs)

class TailwindDateInput(DateInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {"type": "date", "class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"})
        super().__init__(*args, **kwargs)

class TailwindFileInput(FileInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {
            "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none"
        })
        super().__init__(*args, **kwargs)

class TailwindEmailInput(EmailInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {"class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"})
        super().__init__(*args, **kwargs)

class TailwindSelect(Select):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {"class": "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"})
        super().__init__(*args, **kwargs)


class TailwindClearableFileInput(ClearableFileInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = base_classes
        super().__init__(*args, **kwargs)

class TailwindPasswordInput(PasswordInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = base_classes
        super().__init__(*args, **kwargs)

class TailwindURLInput(URLInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = base_classes
        super().__init__(*args, **kwargs)
from modeltranslation.translator import TranslationOptions


class ProductTranslation(TranslationOptions):
    fields = ('name', 'description')

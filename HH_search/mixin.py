import uuid


class HeadHunterParseMixin:
    """
    This class provides handy methods for HeadHunter Service
    """
    def _get_vacancies_on_page(self, souped_page):
        main_content = souped_page.find('div', attrs={'id': "a11y-main-content"})
        vacancy_anchors = main_content.findAll('div', {'class': ['vacancy-serp-item-body__main-info']})
        return self.__parse_hh_vacancy(vacancy_anchors)

    def __parse_hh_vacancy(self, anchors):
        vacancies = []

        for content in anchors:
            link_anchor = content.find('a', attrs={'class': ['bloko-link']})
            link_value = link_anchor['href']
            vacancy_name = link_anchor.text

            cash_info = content.find('span', attrs={'class': ['bloko-header-section-3']})
            if cash_info is None:
                min_salary, max_salary, currency = None, None, None
            else:
                min_salary, max_salary, currency = self.__get_cash_values(cash_info.text)

            try:
                city = content.find('div', attrs={'data-qa': "vacancy-serp__vacancy-address"}).text
            except TypeError:
                city = None

            vacancies.append({
                '_id': str(uuid.uuid4()),
                'vacancy_name': vacancy_name,
                'link': link_value,
                'city': city,
                'min_salary': min_salary,
                'max_salary': max_salary,
                'currency': currency,
            })
        return vacancies

    @staticmethod
    def __get_cash_values(raw_data) -> tuple:
        """
        Parse input string to tuple with 3 elements.
        If some of this elements is not exist, define as None

        Args -> str:
            input_string: string like '100 - 10000 RUB' or something like that

        Returns:
            tuple of min salary, max salary and kind of currency; None for each if empty
        """
        raw_data = raw_data.replace('<!-- -->', '')
        max_salary = None
        min_salary = None
        currency = None

        sep_position = raw_data.find('–')
        if sep_position != -1:
            min_salary = int(''.join([raw_data[i] for i in range(sep_position, -1, -1) if raw_data[i].isdigit()][::-1]))
            max_salary = int(
                ''.join([raw_data[i] for i in range(sep_position, len(raw_data)) if raw_data[i].isdigit()]))
            sep_position = raw_data.rfind(' ')
            currency = ''.join([raw_data[i] for i in range(sep_position, len(raw_data)) if raw_data[i].isalpha()])
            currency = currency if len(currency) > 0 else None
        else:
            sep_position = raw_data.rfind(' ')
            if sep_position != -1:
                if raw_data.find('от') != -1:
                    min_salary = int(
                        ''.join([raw_data[i] for i in range(sep_position, -1, -1) if raw_data[i].isdigit()][::-1]))
                if raw_data.find('до') != -1:
                    max_salary = int(
                        ''.join([raw_data[i] for i in range(sep_position, -1, -1) if raw_data[i].isdigit()][::-1]))
                currency = ''.join([raw_data[i] for i in range(sep_position, len(raw_data)) if raw_data[i].isalpha()])
                currency = currency if len(currency) > 0 else None
            elif len(raw_data) > 0:
                max_salary = ''.join([raw_data[i] for i in range(0, -1, -1) if raw_data[i].isdigit()][::-1])
                max_salary = int(max_salary) if len(max_salary) > 0 else None
                min_salary = max_salary
            else:
                min_salary = max_salary = currency = None
        return min_salary, max_salary, currency

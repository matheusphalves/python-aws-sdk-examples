import re

class TextParser:

    @staticmethod
    def apply_patterns_to_dict(dict, regex_entries):
        """
        Aplica as expressões regulares fornecidas ao valor da chave do dicionário.

        :param dict: Dicionário que possuem dados onde os padrões serão aplicados.
        :param regex_entries: Lista de dicionários contendo o nome do parâmetro, a expressão regular e em qual chave o padrão deve ser aplicado.
        :return: Um dicionário com os parâmetros como chaves e listas de resultados das expressões regulares como valores.
        """
        results = {}

        for matching_input in regex_entries:

            parameter = matching_input.get("parameter")
            regex = matching_input.get("regex")
            targetKey = matching_input.get("targetKey")

            try:
                matches = re.findall(regex, dict[targetKey], re.DOTALL)

                if parameter not in results:
                    results[parameter] = []

                results[parameter].extend(matches)
                
            except Exception as exception:
                print(f'Failed to parse {targetKey} using regex {regex}: {str(exception)}')


        return results
    
    def apply_patterns(string: str, pattern):
        """
        Aplica uma expressão regular a um dado conteúdo textual, retornando os elementos que possuem correspondência.

        :param string: Conteúdo onde o padrão será aplicado.
        :param pattern: A expressão regular que será utilizada.
        :return: Tupla contendo os registros textuais que foram obtidos a partir do padrão aplicado.
        """
        try:

            matches = re.search(pattern, string)

            if matches is None:
                return ()

            return matches.groups()
                
        except Exception as exception:
                raise Exception(f'Failed to parse {string} using pattern {pattern}: {str(exception)}')
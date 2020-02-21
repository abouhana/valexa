import urllib, base64
from os import path

class HtmlWriter:

    def __init__(self, profile_to_use):
        self.profile = profile_to_use

    def write_profile(self, file_name):

        if not self.__valid_if_file_exist(file_name):
            file = open(file_name, 'w')
            file.write('''<!DOCTYPE html>     
                <html>
                <head>
                <style>
                    table, th, td {
                        border: 1px solid black;
                        border-collapse: collapse;
                    }
                </style>
                </head>
                <body>''')
            file.close()

        file = open(file_name, 'a')

        file.write(f'''<table style="border: 1px solid black">
              <tr style="border: 1px solid black">
                <th>Composé</th>
                <th colspan="7">{self.__format_value(self.profile.name_of_file.replace('.xlsx',''))}</th>
              </tr>
              <tr style="border: 1px solid black">
                <td>Modèle</td>
                <td colspan="3">{self.__format_value(self.profile.model.name)}</td>
                <td>beta</td>
                <td>{self.__format_value(self.profile.tolerance_limit)}</td>
                <td>t</td>
                <td>{self.__format_value(self.profile.acceptance_limit)}</td>
              </tr>
              <tr style="border: 1px solid black">
                <td>LOQ Min</td>
                <td colspan="3">{self.__format_value(self.profile.min_lq)}</td>
                <td>LOQ Max</td>
                <td colspan="3">{self.__format_value(self.profile.max_lq)}</td>
              </tr>
              <tr style="border: 1px solid black">
                <td>LOD</td>
                <td colspan="3">{self.__format_value(self.profile.ld)}</td>
                <td>Corr. Factor.</td>
                <td>{self.__format_value(self.profile.model.correction_factor)}</td>
                <td>Recovery</td>
                <td>{self.__calculate_recovery(self.profile.model.correction_factor)}</td>
              </tr>
              <tr style="border: 1px solid black">
                <td colspan="8"></td>
              </tr>
              <tr style="border: 1px solid black">
                <td rowspan="2">Concentration</td>
                <td rowspan="2">Mesuré</td>
                <td colspan="2">Exactitude</td>
                <td colspan="2">Précision</td>
                <td colspan="2">Justesse</td>
              </tr>
              <tr style="border: 1px solid black">
                <td>Biais absolue</td>
                <td>Biais relatif</td>
                <td>Répétabilité (%RSD)</td>
                <td>Intermédiaire (%RSD)</td>
                <td>Limite de tolérance</td>
                <td>Limite relative</td>
              </tr>''')

        for list_item in self.profile.levels:
            file.write(f'''<tr style="border: 1px solid black"> 
                <td>{list_item.introduced_concentration:.3f}</td>
                <td>{list_item.calculated_concentration:.3f}</td>
                <td>{list_item.bias:.3f}</td>
                <td>{list_item.relative_bias:.2f}</td>
                <td>{list_item.repeatability_std_pc:.3f}</td>
                <td>{list_item.inter_series_std_pc:.3f}</td>
                <td>[{list_item.abs_tolerance[0]:.2f},{list_item.abs_tolerance[1]:.2f}]</td>
                <td>[{-100 + list_item.rel_tolerance[0]:.2f},{-100 + list_item.rel_tolerance[1]:.2f}]</td>
              </tr>''')

        self.profile.image_data.seek(0)

        image_string = base64.b64encode(self.profile.image_data.read())
        uri = 'data:image/png;base64,' + urllib.parse.quote(image_string)
        file.write(f'''<tr style="border: 1px solid black">
                        <td colspan="8"></td>
                      </tr>
                      <tr style="border: 1px solid black">
                        <td colspan="8"><img src = "{uri}"/></td>
                      </tr>
                    </table>
                    <br>''')
        file.close()

    def __valid_if_file_exist(self, file_name):
        return path.exists(file_name)

    def __format_value(self, value_to_format):
        if value_to_format is None:
            return 'N/A'
        elif isinstance(value_to_format, float):
            return '{0:.3f}'.format(value_to_format)
        else:
            return value_to_format

    def __calculate_recovery(self, correction_factor):
        if correction_factor is None:
            return 'N/A'
        else:
            return '{0:.2f}'.format(1/correction_factor*100)

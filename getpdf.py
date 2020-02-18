from requests import get
from urllib.parse import urljoin
from os import path, getcwd
from bs4 import BeautifulSoup as soup
import sys
import logging



def get_page(base_url):
  req = get(base_url)
  if req.status_code == 200:
      return req.text
  logging.warning('http status_code: ' + req.status_code)
  raise Exception('Error {0}'.format(req.status_code))

def get_all_links(html):
  bs = soup(html, 'html.parser')  # MISSING 'html.parser'
  print(bs.prettify())
  links = bs.findAll('a')
  links = links[1:]
  return links

def get_links_to_nav(base_url):
  html = get_page(base_url)  # MISSING ARGUMENT
  links = get_all_links(html)

  if len(links) == 0:
      logging.warning('No links found on the webpage.')
      raise Exception('No links found on the webpage')
  return links

def get_name(text):
  tmp = ''
  if (len(text) > 50):
    tmp = text[:50]
    tmp2 = tmp[-4:]
    print(tmp2)
    print(tmp)
      if (tmp2 != '.pdf'):
        tmp = tmp + '.pdf'
        
  return tmp


def get_pdf(base_url, base_dir):
  logging.basicConfig(filename=path.join(base_dir, 'downloads_log.log'), level=logging.INFO, format='%(asctime)s %(message)s')
  logging.info('------------------------------------------------------------------------------------------')
  logging.info('')
  logging.info('')
  logging.info('Starting')
  logging.info('base_url: ' + base_url)
  logging.info('base_dir: ' + base_dir)

  html = get_page(base_url)  # MISSING ARGUMENT
  links = get_all_links(html)
  if len(links) == 0:
      logging.warning('No links found on the webpage.')
      raise Exception('No links found on the webpage')

  n_pdfs = 0
  n_saved_pdfs = 0

  for link in links:
      current_link = link.get('href')  # This line and the line below
      text = link.contents
      name = get_name(text[0])
      if current_link.endswith('pdf'):
          weblink = urljoin(base_url, link['href'])
          logging.info('pdf file found at ' + weblink)
          print('pdf file found:', weblink)

          n_pdfs += 1

          file_address = path.join(base_dir, name)

          if path.exists(file_address) == False:
              content = get(weblink, stream=True)  # https://stackoverflow.com/a/44299915/2449724
              # stream=True means when function returns, only the response header is downloaded, response body is not.

              if content.status_code == 200 and content.headers[
                  'content-type'] == 'application/pdf':  # status to status_code
                  print('File size(mb)', round(float(content.headers['Content-length']) / 1000000), 2, sep=',')
                  with open(file_address, 'wb') as pdf:
                      logging.info('Saving pdf to ' + file_address)
                      print('Saving pdf to', file_address)

                      pdf.write(content.content)

                      logging.info('COMPLETE')
                      print('COMPLETE')

                      n_saved_pdfs += 1
                      logging.info('Number of save pdfs is ' + str(n_saved_pdfs))
                      print()
              else:
                  logging.info('content.status_code: ' + str(content.status_code))
                  logging.info('''content.headers['content-type']:''' + content.headers['content-type'])
                  print('content.status_code:', content.status_code)
                  print('''content.headers['content-type']:''', content.headers['content-type'])
                  print()

          else:
              logging.info('Already saved.')
              print('Already saved')
              n_saved_pdfs += 1
              print()
      if n_pdfs == 0:
          logging.info('No pdfs found on the page.')

      logging.info("{0} pdfs found, {1} saved in {2}".format(n_pdfs, n_saved_pdfs, base_dir))
      print("{0} pdfs found, {1} saved in {2}".format(n_pdfs, n_saved_pdfs, base_dir))

def get_all_sessions(base_url, url, base_dir):
  links = get_links_to_nav(url)
  for link in links:
    #Años 2013-2018
    current_link = link.get('href')
    current_link = base_url + current_link
    meses = get_links_to_nav(current_link)
    #meses = meses[1:]
    for mes in meses:
      #Meses del año correspondiente
      current_mes = mes.get('href')
      current_mes = base_url + current_mes
      sesiones = get_links_to_nav(current_mes)
      #sesiones = sesiones[1:]
      for sesion in sesiones:
        #sesion actual 
        sesion_link = sesion.get('href')
        sesion_link = base_url + sesion_link
        get_pdf(sesion_link, base_dir)


if __name__ == "__main__":
  base_url = ''
  base_dir = '' #example r'C:\User'

  if base_dir or base_url:
      print('Please, assign values to base_url and base_dir.')

  base_url = 'http://guest:guest@documentacion.asambleanacional.gob.ec'
  url = 'http://guest:guest@documentacion.asambleanacional.gob.ec/alfresco/webdav/Documentos%20Web/Votaciones%20del%20Pleno'
  base_dir = 'pdfs/'
  #get_pdf(base_url,base_dir)
  get_all_sessions(base_url, url, base_dir)

  
  #documento = http://guest:guest@documentacion.asambleanacional.gob.ec/alfresco/webdav/Documentos%20Web/Votaciones%20del%20Pleno
  '''
  el primer enlace esta compuesto de años 2013-2020
  /Documentos Web/Votaciones del Pleno/Año 2013/ 
  compuesto de meses (cualquier mes)
  /Documentos Web/Votaciones del Pleno/Año 2013/Mayo/
  compuesto de sesiones
  /Documentos Web/Votaciones del Pleno/Año 2013/Mayo/Sesión 00 del Pleno instalación (14-05-2013)/
  compuesto de pdfs
  '''
  años = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
  Asize = 8


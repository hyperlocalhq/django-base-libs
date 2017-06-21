# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0007_auto_20160926_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='establishment_yyyy',
            field=models.IntegerField(blank=True, null=True, verbose_name='Year of Establishment', choices=[(2017, 2017), (2016, 2016), (2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999), (1998, 1998), (1997, 1997), (1996, 1996), (1995, 1995), (1994, 1994), (1993, 1993), (1992, 1992), (1991, 1991), (1990, 1990), (1989, 1989), (1988, 1988), (1987, 1987), (1986, 1986), (1985, 1985), (1984, 1984), (1983, 1983), (1982, 1982), (1981, 1981), (1980, 1980), (1979, 1979), (1978, 1978), (1977, 1977), (1976, 1976), (1975, 1975), (1974, 1974), (1973, 1973), (1972, 1972), (1971, 1971), (1970, 1970), (1969, 1969), (1968, 1968), (1967, 1967), (1966, 1966), (1965, 1965), (1964, 1964), (1963, 1963), (1962, 1962), (1961, 1961), (1960, 1960), (1959, 1959), (1958, 1958), (1957, 1957), (1956, 1956), (1955, 1955), (1954, 1954), (1953, 1953), (1952, 1952), (1951, 1951), (1950, 1950), (1949, 1949), (1948, 1948), (1947, 1947), (1946, 1946), (1945, 1945), (1944, 1944), (1943, 1943), (1942, 1942), (1941, 1941), (1940, 1940), (1939, 1939), (1938, 1938), (1937, 1937), (1936, 1936), (1935, 1935), (1934, 1934), (1933, 1933), (1932, 1932), (1931, 1931), (1930, 1930), (1929, 1929), (1928, 1928), (1927, 1927), (1926, 1926), (1925, 1925), (1924, 1924), (1923, 1923), (1922, 1922), (1921, 1921), (1920, 1920), (1919, 1919), (1918, 1918), (1917, 1917), (1916, 1916), (1915, 1915), (1914, 1914), (1913, 1913), (1912, 1912), (1911, 1911), (1910, 1910), (1909, 1909), (1908, 1908), (1907, 1907), (1906, 1906), (1905, 1905), (1904, 1904), (1903, 1903), (1902, 1902), (1901, 1901), (1900, 1900), (1899, 1899), (1898, 1898), (1897, 1897), (1896, 1896), (1895, 1895), (1894, 1894), (1893, 1893), (1892, 1892), (1891, 1891), (1890, 1890), (1889, 1889), (1888, 1888), (1887, 1887), (1886, 1886), (1885, 1885), (1884, 1884), (1883, 1883), (1882, 1882), (1881, 1881), (1880, 1880), (1879, 1879), (1878, 1878), (1877, 1877), (1876, 1876), (1875, 1875), (1874, 1874), (1873, 1873), (1872, 1872), (1871, 1871), (1870, 1870), (1869, 1869), (1868, 1868), (1867, 1867), (1866, 1866), (1865, 1865), (1864, 1864), (1863, 1863), (1862, 1862), (1861, 1861), (1860, 1860), (1859, 1859), (1858, 1858), (1857, 1857), (1856, 1856), (1855, 1855), (1854, 1854), (1853, 1853), (1852, 1852), (1851, 1851), (1850, 1850), (1849, 1849), (1848, 1848), (1847, 1847), (1846, 1846), (1845, 1845), (1844, 1844), (1843, 1843), (1842, 1842), (1841, 1841), (1840, 1840), (1839, 1839), (1838, 1838), (1837, 1837), (1836, 1836), (1835, 1835), (1834, 1834), (1833, 1833), (1832, 1832), (1831, 1831), (1830, 1830), (1829, 1829), (1828, 1828), (1827, 1827), (1826, 1826), (1825, 1825), (1824, 1824), (1823, 1823), (1822, 1822), (1821, 1821), (1820, 1820), (1819, 1819), (1818, 1818)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='institutionalcontact',
            name='validity_end_yyyy',
            field=models.IntegerField(blank=True, null=True, verbose_name='Till Year', choices=[(2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='institutionalcontact',
            name='validity_start_yyyy',
            field=models.IntegerField(blank=True, null=True, verbose_name='From Year', choices=[(2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026)]),
            preserve_default=True,
        ),
    ]

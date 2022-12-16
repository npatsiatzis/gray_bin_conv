--Binary to gray code converter.

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity bin_to_gray is
	generic (
	 		g_width : natural := 8);
	 	port (
	 	 		i_bin : in std_ulogic_vector(g_width-1 downto 0);
	 	 		o_gray  : out std_ulogic_vector(g_width-1 downto 0)); 
end bin_to_gray;

architecture converter of bin_to_gray is 
begin
	o_gray <= std_ulogic_vector(shift_right(unsigned(i_bin),1)) xor i_bin;
end converter;
--Gray to binary code converter

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity gray_to_bin is
	generic(
		g_width : natural :=8);
  	port (
		i_gray : in std_ulogic_vector(g_width-1 downto 0);
		o_bin : out std_ulogic_vector(g_width-1 downto 0));
end gray_to_bin ; -- bin_to_gray

architecture converter of gray_to_bin is
begin
	bin2gray_covnert : for i in 0 to g_width-1 generate
		o_bin(i) <= xor(shift_right(unsigned(i_gray),i));
	end generate;
end converter;
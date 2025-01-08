from math import log

class Expr:
	def back(self):
		pass
	
	def backward(self):
		self.zero()
		self.back(1)

	def __mul__(self, b):
		if not isinstance(b, Expr):
			b = Num(b)
		return Mul(self, b)

	def __rmul__(self, b):
		return self * b

	def __add__(self, b):
		if not isinstance(b, Expr):
			b = Num(b)
		return Add(self, b)

	def __radd__(self, b):
		return self + b

	def __sub__(self, b):
		if not isinstance(b, Expr):
			b = Num(b)
		b *= -1
		return Add(self, b)

	def __neg__(self):
		return self*(-1)
	
	def __pow__(self, b):
		if not isinstance(b, Expr):
			b = Num(b)
		return Pow(self, b)

	def __rpow__(self, b):
		return Num(b)**self

class Num(Expr):
	def __init__(self, value):
		self.value = value
		self.grad = 0

	def back(self, upstream):
		self.grad += upstream

	def zero(self):
		self.grad = 0

class Add(Expr):
	def __init__(self, a, b):
		self.a = a
		self.b = b
		self.value = a.value + b.value

	def back(self, upstream):
		self.a.back(upstream)
		self.b.back(upstream)

	def zero(self):
		self.a.zero()
		self.b.zero()

class Mul(Expr):
	def __init__(self, a, b):
		self.a = a
		self.b = b
		self.value = a.value * b.value
	
	def back(self, upstream):
		self.a.back(self.b.value * upstream)
		self.b.back(self.a.value * upstream)

	def zero(self):
		self.a.zero()
		self.b.zero()

class Pow(Expr):
	def __init__(self, base, exp):
		self.value = base.value ** exp.value
		self.base = base
		self.exp = exp

	def back(self, upstream):
		self.base.back(self.value * self.exp.value / self.base.value * upstream)
		self.exp.back(self.value * log(self.base.value) * upstream)

	def zero(self):
		self.base.zero()
		self.exp.zero()

class Max(Expr):
	def __init__(self, a, b):
		self.value = max(a.value, b.value)
		self.a = a
		self.b = b
	
	def zero(self):
		self.a.zero()
		self.b.zero()

	def back(self, upstream):
		if self.a.value > self.b.value:
			self.a.back(upstream)
		else:
			self.b.back(upstream)


class Min(Expr):
	def __init__(self, a, b):
		self.value = min(a.value, b.value)
		self.a = a
		self.b = b
	
	def zero(self):
		self.a.zero()
		self.b.zero()

	def back(self, upstream):
		if self.a.value < self.b.value:
			self.a.back(upstream)
		else:
			self.b.back(upstream)

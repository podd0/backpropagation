class Expr:
	def back(self):
		pass
	
	def backward(self):
		self.zero()
		self.grad = 1
		self.back()

	def __mul__(self, b):
		if not isinstance(b, Expr):
			b = Num(b)
		return Mul(self, b)

	def __add__(self, b):
		if not isinstance(b, Expr):
			b = Num(b)
		return Add(self, b)

class Num(Expr):
	def __init__(self, value):
		self.value = value
		self.grad = 0

	def back(self):
		return super().back()

	def zero(self):
		self.grad = 0

class Add(Expr):
	def __init__(self, a, b):
		self.a = a
		self.b = b
		self.value = a.value + b.value
		self.grad = 1

	def back(self):
		self.a.grad += self.grad
		self.b.grad += self.grad
		self.a.back()
		self.b.back()

	def zero(self):
		self.grad = 0
		self.a.zero()
		self.b.zero()

class Mul(Expr):
	def __init__(self, a, b):
		self.a = a
		self.b = b
		self.value = a.value * b.value
	
	def back(self):
		self.a.grad += self.b.value * self.grad
		self.a.back()
		self.b.grad += self.a.value * self.grad
		self.b.back()

	def zero(self):
		self.grad = 0
		self.a.zero()
		self.b.zero()

